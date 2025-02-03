# Copyright 2024 Rebellions Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Portions of this software are licensed under the Apache License,
# Version 2.0. See the NOTICE file distributed with this work for
# additional information regarding copyright ownership.

# All other portions of this software, including proprietary code,
# are the intellectual property of Rebellions Inc. and may not be
# copied, modified, or distributed without prior written permission
# from Rebellions Inc.

import logging
import os
import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional, Union

import rebel
import torch
from huggingface_hub import HfApi, HfFolder, hf_hub_download
from optimum.exporters import TasksManager
from optimum.modeling_base import OptimizedModel
from transformers import (
    AutoConfig,
    AutoModel,
    AutoModelForAudioClassification,
    AutoModelForImageClassification,
    AutoModelForQuestionAnswering,
    GenerationConfig,
    PretrainedConfig,
)

from .modeling_config import DEFAULT_COMPILED_MODEL_NAME, RBLNConfig, RBLNRuntimeConfig
from .utils.runtime_utils import UnavailableRuntime
from .utils.save_utils import maybe_load_preprocessors, maybe_save_preprocessors


logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from transformers import AutoFeatureExtractor, AutoProcessor, AutoTokenizer, PreTrainedModel


class RBLNBaseModel(OptimizedModel, ABC):
    """
    An abstract base class for compiling, loading, and saving neural network models from the huggingface
    transformers and diffusers libraries to run on RBLN NPU devices.

    This class supports loading and saving models using the `from_pretrained` and `save_pretrained` methods,
    similar to the huggingface libraries.

    The `from_pretrained` method loads a model corresponding to the given `model_id` from a local repository
    or the huggingface hub onto the NPU. If the model is a PyTorch model and `export=True` is passed as a
    kwarg, it compiles the PyTorch model corresponding to the given `model_id` before loading. If `model_id`
    is an already rbln-compiled model, it can be directly loaded onto the NPU with `export=False`.

    `rbln_npu` is a kwarg required for compilation, specifying the name of the NPU to be used. If this
    keyword is not specified, the NPU installed on the host machine is used. If no NPU is installed on the
    host machine, an error occurs.

    `rbln_device` specifies the device to be used at runtime. If not specified, device 0 is used.

    `rbln_create_runtimes` indicates whether to create runtime objects. If False, the runtime does not load
    the model onto the NPU. This option is particularly useful when you want to perform compilation only on a
    host machine without an NPU.

    `RBLNModel`, `RBLNModelFor*`, etc. are all child classes of RBLNBaseModel.

    Models compiled in this way can be saved to a local repository using `save_pretrained` or uploaded to
    the huggingface hub.

    It also supports generation through `generate` (for transformers models that support generation).

    RBLNBaseModel is a class for models consisting of an arbitrary number of `torch.nn.Module`s, and
    therefore is an abstract class without explicit implementations of `forward` or `export` functions.
    To inherit from this class, `forward`, `export`, etc. must be implemented.
    """

    model_type = "rbln_model"
    auto_model_class = AutoModel  # feature extraction
    config_name = "config.json"

    def __init__(
        self,
        models: List[rebel.Runtime],
        config: "PretrainedConfig",
        rbln_config: RBLNConfig,
        preprocessors: Optional[List],
        model_save_dir: Optional[Union[str, Path, TemporaryDirectory]] = None,
        subfolder: str = "",
        rbln_compiled_models: Optional[rebel.RBLNCompiledModel] = None,
        **kwargs,
    ):
        super().__init__(models, config)
        if not isinstance(self.config, PretrainedConfig):  # if diffusers config
            self.config = PretrainedConfig(**self.config)

        self.rbln_config = rbln_config
        self.preprocessors = [] if preprocessors is None else preprocessors
        self.compiled_models = rbln_compiled_models

        # Registers the RBLNBaseModelForXXX classes into the transformers AutoModel classes to avoid warnings when creating
        # a pipeline https://github.com/huggingface/transformers/blob/3d3204c025b6b5de013e07dd364208e28b4d9589/src/transformers/pipelines/base.py#L940
        AutoConfig.register(self.model_type, AutoConfig)
        if hasattr(self.auto_model_class, "register"):
            self.auto_model_class.register(AutoConfig, self.__class__)

        # copied from tranformers PreTrainedModel __init__
        self.generation_config = GenerationConfig.from_model_config(config) if self.can_generate() else None
        if self.generation_config is not None:
            self.generation_config.use_cache = True

        self.device = torch.device("cpu")

        # FIXME :: model_save_dir is not used after initialized. (This can be used when save/load)
        # This attribute is needed to keep one reference on the temporary directory, since garbage collecting it
        # would end-up removing the directory containing the underlying RBLN model.
        self._model_save_dir_tempdirectory_instance = None
        if isinstance(model_save_dir, TemporaryDirectory):
            self._model_save_dir_tempdirectory_instance = model_save_dir
            self.model_save_dir = Path(model_save_dir.name)
        elif isinstance(model_save_dir, str):
            self.model_save_dir = Path(model_save_dir)
        else:
            self.model_save_dir = model_save_dir
        self.subfolder = subfolder

        self.__post_init__(**kwargs)

    def __post_init__(self, **kwargs):
        pass

    def _save_pretrained(self, save_directory: Union[str, Path]):
        """
        Saves a model and its configuration file to a directory, so that it can be re-loaded using the
        [`~optimum.rbln.modeling_base.RBLNBaseModel.from_pretrained`] class method.

        Args:
            save_directory (`Union[str, Path]`):
                Directory where to save the model file.
        """
        real_save_dir = self.model_save_dir / self.subfolder
        if os.path.exists(real_save_dir) and os.path.isdir(real_save_dir):
            shutil.copytree(real_save_dir, save_directory, dirs_exist_ok=True)
            self.config.save_pretrained(save_directory)
            if self.generation_config is not None:
                self.generation_config.save_pretrained(save_directory)
        else:
            raise FileNotFoundError(f"Saving compiled model failed.({real_save_dir}).")

    @classmethod
    def _from_pretrained(
        cls,
        model_id: Union[str, Path],
        config: "PretrainedConfig",
        use_auth_token: Optional[Union[bool, str]] = None,
        revision: Optional[str] = None,
        force_download: bool = False,
        cache_dir: Optional[str] = None,
        subfolder: str = "",
        local_files_only: bool = False,
        model_save_dir: Optional[Union[str, Path, TemporaryDirectory]] = None,
        # Runtime - related kwargs
        rbln_device: Optional[List[int]] = None,
        rbln_device_map: Optional[Dict[str, int]] = None,
        rbln_create_runtimes: Optional[bool] = None,
        # passed from compile function
        rbln_config: Optional[RBLNConfig] = None,
        rbln_compiled_models: Optional[List[rebel.RBLNCompiledModel]] = None,
        rbln_optimize_host_memory: Optional[bool] = None,
        **kwargs,
    ) -> "RBLNBaseModel":
        model_path = Path(model_id)
        if model_path.is_dir():
            model_path = model_path / subfolder
            rbln_files = list(model_path.glob("*.rbln"))
            rbln_config_filenames = list(model_path.glob("rbln_config.json"))
        else:
            if isinstance(use_auth_token, bool):
                token = HfFolder().get_token()
            else:
                token = use_auth_token
            repo_files = list(map(Path, HfApi().list_repo_files(model_id, revision=revision, token=token)))

            pattern = "*.rbln" if subfolder == "" else f"{subfolder}/*.rbln"
            rbln_files = [p for p in repo_files if p.match(pattern)]

            pattern = "rbln_config.json" if subfolder == "" else f"{subfolder}/rbln_config.json"
            rbln_config_filenames = [p for p in repo_files if p.match(pattern)]

        if len(rbln_files) == 0:
            raise FileNotFoundError(f"Could not find any rbln model file in {model_path}")

        if len(rbln_config_filenames) == 0:
            raise FileNotFoundError(f"Could not find `rbln_config.json` file in {model_path}")

        if len(rbln_config_filenames) > 1:
            raise FileExistsError(
                f"Multiple rbln_config.json are not expected. but {len(rbln_config_filenames)} are found."
            )

        if model_path.is_dir():
            if rbln_compiled_models is None:
                rbln_config = RBLNConfig.load(str(model_path))
                rbln_compiled_models = [
                    rebel.RBLNCompiledModel(model_path / f"{compiled_model_name}.rbln")
                    for compiled_model_name in rbln_config
                ]
                new_model_save_dir = model_path
            else:
                pass

        else:
            rbln_config_filename = rbln_config_filenames[0]
            rbln_config_cache_path = hf_hub_download(
                repo_id=model_id,
                filename=str(rbln_config_filename),
                subfolder=subfolder,
                use_auth_token=use_auth_token,
                revision=revision,
                cache_dir=cache_dir,
                force_download=force_download,
                local_files_only=local_files_only,
            )
            rbln_config = RBLNConfig.load(Path(rbln_config_cache_path).parent)
            rbln_compiled_models = []
            for compiled_model_name in rbln_config:
                model_cache_path = hf_hub_download(
                    repo_id=model_id,
                    filename=f"{compiled_model_name}.rbln",
                    subfolder=subfolder,
                    use_auth_token=use_auth_token,
                    revision=revision,
                    cache_dir=cache_dir,
                    force_download=force_download,
                    local_files_only=local_files_only,
                )
                rbln_compiled_models.append(rebel.RBLNCompiledModel(model_cache_path))
            new_model_save_dir = Path(rbln_config_cache_path).parent

        preprocessors = maybe_load_preprocessors(model_id, subfolder=subfolder)

        if model_save_dir is None:
            model_save_dir = new_model_save_dir

        # Create runtimes
        if rbln_create_runtimes is None:
            rbln_create_runtimes = rebel.npu_is_available()
        if rbln_device_map is None:
            rbln_device_map = {}
            device_val = 0 if rbln_device is None else rbln_device
            for key in rbln_config:
                rbln_device_map[key] = device_val
        else:
            rbln_device_map = rbln_device_map

        # create runtimes only if `rbln_create_runtimes` is enabled
        models = (
            cls._create_runtimes(rbln_compiled_models, rbln_device_map)
            if rbln_create_runtimes
            else UnavailableRuntime()
        )

        if rbln_optimize_host_memory is None:
            rbln_optimize_host_memory = True

        return cls(
            models,
            config,
            rbln_config,
            preprocessors,
            model_save_dir=model_save_dir,
            subfolder=subfolder,
            rbln_compiled_models=None if rbln_optimize_host_memory else rbln_compiled_models,
            **kwargs,
        )

    def __repr__(self):
        return repr(self.model)

    @classmethod
    def compile(cls, model, rbln_runtime_config: Optional[RBLNRuntimeConfig] = None):
        compiled_model = rebel.compile_from_torch(
            model,
            input_info=rbln_runtime_config.input_info,
            batch_size=rbln_runtime_config.batch_size,
            fusion=rbln_runtime_config.fusion,
            npu=rbln_runtime_config.npu,
            tensor_parallel_size=rbln_runtime_config.tensor_parallel_size,
        )
        return compiled_model

    @classmethod
    def get_rbln_config(
        cls,
        **rbln_config_kwargs,
    ) -> RBLNConfig:
        """
        Make default rbln-config for the model.

        if `input_info` specified,
            other kwargs but `input_info`, `batch_size` and `fusion` are ignored.

        kwargs for overriding model's config can be accepted.

        Note that batch_size should be specified with proper input_info.
        """

        input_info = rbln_config_kwargs.pop("rbln_input_info", None)
        batch_size = rbln_config_kwargs.pop("rbln_batch_size", None)
        fusion = rbln_config_kwargs.pop("rbln_fusion", None)
        npu = rbln_config_kwargs.pop("rbln_npu", None)
        tensor_parallel_size = rbln_config_kwargs.pop("rbln_tensor_parallel_size", None)

        if input_info is not None:
            rbln_runtime_config = RBLNRuntimeConfig(
                input_info=input_info,
                batch_size=batch_size,
                fusion=fusion,
                npu=npu,
                tensor_parallel_size=tensor_parallel_size,
            )
            rbln_config = RBLNConfig.from_rbln_runtime_configs([rbln_runtime_config])
        else:
            rbln_config = cls._get_rbln_config(rbln_batch_size=batch_size, **rbln_config_kwargs)
            for k, rcfgs in rbln_config.items():
                for rcfg in rcfgs:
                    rcfg: RBLNRuntimeConfig
                    rcfg.fusion = fusion
                    rcfg.npu = npu
                    rcfg.tensor_parallel_size = tensor_parallel_size

        return rbln_config

    @staticmethod
    def pop_rbln_kwargs_from_kwargs(kwargs: dict):
        keys = list(kwargs.keys())
        rbln_constructor_kwargs = {
            key: kwargs.pop(key)
            for key in keys
            if key
            in [
                "rbln_device",
                "rbln_device_map",
                "rbln_create_runtimes",
                "rbln_optimize_host_memory",
            ]
        }

        keys = list(kwargs.keys())
        rbln_config_kwargs = {key: kwargs.pop(key) for key in keys if key.startswith("rbln_")}
        return rbln_config_kwargs, rbln_constructor_kwargs

    def can_generate(self):
        return False

    def to(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return self.forward(*args, **kwargs)

    @classmethod
    def wrap_model_if_needed(cls, model: torch.nn.Module) -> torch.nn.Module:
        # Wrap the model if needed.
        return model

    @classmethod
    def _from_transformers(cls, *args, **kwargs) -> "RBLNBaseModel":
        """
        Exports a vanilla Transformers model into a rbln-compiled Module.
        This will be deprecated after optimum 2.0
        """
        return cls._export(*args, **kwargs)

    @classmethod
    def _get_rbln_config(cls, **rbln_config_kwargs) -> RBLNConfig:
        raise NotImplementedError

    @abstractmethod
    def forward(self, *args: List[torch.Tensor], **kwargs: Dict[str, torch.Tensor]):
        pass

    @classmethod
    @abstractmethod
    def _create_runtimes(
        cls, compiled_models: List[rebel.RBLNCompiledModel], rbln_device_map: Dict[str, int]
    ) -> List[rebel.Runtime]:
        # compiled_models -> runtimes
        pass

    @classmethod
    @abstractmethod
    def _export(
        cls,
        model_id: Union[str, Path],
        config: "PretrainedConfig",
        use_auth_token: Optional[Union[bool, str]] = None,
        revision: Optional[str] = None,
        force_download: bool = False,
        cache_dir: Optional[str] = None,
        subfolder: str = "",
        local_files_only: bool = False,
        trust_remote_code: bool = False,
        model_save_dir: Optional[Union[str, Path, TemporaryDirectory]] = None,
        **kwargs,
    ):
        """
        Exports a vanilla Transformers model into a rbln-compiled Module.
        """
        pass


class RBLNModel(RBLNBaseModel):
    """
    A class that inherits from RBLNBaseModel for models consisting of a single `torch.nn.Module`.

    This class supports all the functionality of RBLNBaseModel, including loading and saving models using
    the `from_pretrained` and `save_pretrained` methods, compiling PyTorch models for execution on RBLN NPU
    devices.

    Example:
        ```python
        model = RBLNModel.from_pretrained("model_id", export=True, rbln_npu="npu_name")
        outputs = model(**inputs)
        ```
    """

    @classmethod
    def update_kwargs(cls, kwargs):
        """
        Update user-given kwargs to get proper pytorch model.

        For example, `torchscript`=True should be set because torch.jit
        does not support `transformers` output instances as module output;
        """
        kwargs.update(
            {
                "torchscript": True,
                "return_dict": False,
            }
        )
        return kwargs

    @classmethod
    def get_pytorch_model(
        cls,
        model_id: str,
        use_auth_token: Optional[Union[bool, str]] = None,
        revision: Optional[str] = None,
        force_download: bool = False,
        cache_dir: Optional[str] = None,
        subfolder: str = "",
        local_files_only: bool = False,
        trust_remote_code: bool = False,
        rbln_config_kwargs: Optional[Dict[str, Any]] = None,
        rbln_constructor_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> "PreTrainedModel":
        task = kwargs.pop("task", None)
        if task is None:
            task = TasksManager.infer_task_from_model(cls.auto_model_class)

        kwargs = cls.update_kwargs(kwargs)

        model = TasksManager.get_model_from_task(
            task=task,
            model_name_or_path=model_id,
            subfolder=subfolder,
            revision=revision,
            framework="pt",
            cache_dir=cache_dir,
            use_auth_token=use_auth_token,
            local_files_only=local_files_only,
            force_download=force_download,
            trust_remote_code=trust_remote_code,
            **kwargs,
        )

        return model

    @classmethod
    def get_compiled_model(cls, model: "PreTrainedModel", rbln_config: RBLNConfig):
        model = cls.wrap_model_if_needed(model)
        rbln_runtime_configs = list(rbln_config.values())
        if len(rbln_runtime_configs) != 1:
            raise ValueError
        rbln_runtime_config = rbln_runtime_configs[0]
        if len(rbln_runtime_config) != 1:
            raise ValueError
        rbln_runtime_config = rbln_runtime_config[0]

        compiled_model = cls.compile(model, rbln_runtime_config=rbln_runtime_config)
        return compiled_model

    @classmethod
    @torch.no_grad()
    def _export(
        cls,
        model_id: str,
        config: "PretrainedConfig",
        use_auth_token: Optional[Union[bool, str]] = None,
        revision: Optional[str] = None,
        force_download: bool = False,
        cache_dir: Optional[str] = None,
        subfolder: str = "",
        local_files_only: bool = False,
        trust_remote_code: bool = False,
        model_save_dir: Optional[Union[str, Path, TemporaryDirectory]] = None,
        **kwargs,
    ) -> "RBLNModel":
        if model_save_dir is None:
            save_dir = TemporaryDirectory()
            save_dir_path = Path(save_dir.name)
        else:
            save_dir = model_save_dir
            if isinstance(save_dir, TemporaryDirectory):
                save_dir_path = Path(model_save_dir.name)
            else:
                save_dir_path = Path(model_save_dir)
                save_dir_path.mkdir(exist_ok=True)

        rbln_config_kwargs, rbln_constructor_kwargs = cls.pop_rbln_kwargs_from_kwargs(kwargs)

        model: "PreTrainedModel" = cls.get_pytorch_model(
            model_id=model_id,
            subfolder=subfolder,
            revision=revision,
            cache_dir=cache_dir,
            use_auth_token=use_auth_token,
            local_files_only=local_files_only,
            force_download=force_download,
            trust_remote_code=trust_remote_code,
            rbln_config_kwargs=rbln_config_kwargs,
            rbln_constructor_kwargs=rbln_constructor_kwargs,
            **kwargs,
        )

        # FIXME :: optimum passes AutoConfig.
        config = model.config

        if not isinstance(config, PretrainedConfig):  # diffusers config
            config = PretrainedConfig(**config)

        config.save_pretrained(save_dir_path / subfolder)
        preprocessors = maybe_save_preprocessors(model_id, save_dir_path, src_subfolder=subfolder)

        # Get compilation arguments
        if (rbln_config := rbln_config_kwargs.pop("rbln_config", None)) is None:
            rbln_config = cls.get_rbln_config(preprocessors=preprocessors, model_config=config, **rbln_config_kwargs)
        compiled_model = cls.get_compiled_model(model, rbln_config=rbln_config)

        # Save compiled models
        (save_dir_path / subfolder).mkdir(exist_ok=True)
        if isinstance(compiled_model, Iterable):
            # compiled_model is an Iterable instance
            for single_compiled_model, compiled_model_name in zip(compiled_model, rbln_config):
                single_compiled_model.save(save_dir_path / subfolder / f"{compiled_model_name}.rbln")
            compiled_models = compiled_model

        else:
            compiled_model.save(save_dir_path / subfolder / f"{DEFAULT_COMPILED_MODEL_NAME}.rbln")
            compiled_models = [compiled_model]
        rbln_config.save(save_dir_path / subfolder)

        # Instantiate
        return cls._from_pretrained(
            model_id=save_dir_path,
            config=config,
            model_save_dir=save_dir,
            use_auth_token=use_auth_token,
            revision=revision,
            force_download=force_download,
            cache_dir=cache_dir,
            subfolder=subfolder,
            local_files_only=local_files_only,
            rbln_config=rbln_config,
            rbln_compiled_models=compiled_models,
            **rbln_constructor_kwargs,
            **kwargs,
        )

    @classmethod
    def _create_runtimes(
        cls, compiled_models: List[rebel.RBLNCompiledModel], rbln_device_map: Dict[str, int]
    ) -> List[rebel.Runtime]:
        device = rbln_device_map[DEFAULT_COMPILED_MODEL_NAME]
        return [compiled_model.create_runtime(tensor_type="pt", device=device) for compiled_model in compiled_models]

    def forward(self, *args: List[torch.Tensor], **kwargs: Dict[str, torch.Tensor]):
        output = self.model[0](*args, **kwargs)
        return output


class RBLNModelForQuestionAnswering(RBLNModel):
    model_type = "rbln_model"
    auto_model_class = AutoModelForQuestionAnswering

    @classmethod
    def _get_rbln_config(
        cls,
        preprocessors: Optional[Union["AutoFeatureExtractor", "AutoProcessor", "AutoTokenizer"]],
        model_config: Optional["PretrainedConfig"] = None,
        rbln_max_seq_len: Optional[int] = None,
        rbln_model_input_names: Optional[List[str]] = None,
        rbln_batch_size: Optional[int] = None,
    ) -> RBLNConfig:
        if rbln_max_seq_len is None:
            for tokenizer in preprocessors:
                if hasattr(tokenizer, "model_max_length"):
                    rbln_max_seq_len = tokenizer.model_max_length
                    break
            if rbln_max_seq_len is None:
                raise ValueError("`rbln_max_seq_len` should be specified!")

        if rbln_model_input_names is None:
            # These are BERT's inputs
            rbln_model_input_names = ["input_ids", "attention_mask", "token_type_ids"]

        if rbln_batch_size is None:
            rbln_batch_size = 1
        input_info = [
            (model_input_name, [rbln_batch_size, rbln_max_seq_len], "int64")
            for model_input_name in rbln_model_input_names
        ]

        rbln_runtime_config = RBLNRuntimeConfig(input_info=input_info)
        rbln_runtime_config.batch_size = rbln_batch_size
        meta = {"rbln_max_seq_len": rbln_max_seq_len}

        return RBLNConfig.from_rbln_runtime_configs([rbln_runtime_config], _rbln_meta=meta)


class RBLNModelForImageClassification(RBLNModel):
    """
    This is a generic model class that will be instantiated as one of the model classes of the library (with a image classification head) when created with the from_pretrained() class method
    """

    model_type = "rbln_model"
    auto_model_class = AutoModelForImageClassification

    @classmethod
    def _get_rbln_config(
        cls,
        preprocessors: Optional[Union["AutoFeatureExtractor", "AutoProcessor", "AutoTokenizer"]],
        model_config: Optional["PretrainedConfig"] = None,
        rbln_image_size: Optional[int] = None,
        rbln_batch_size: Optional[int] = None,
    ) -> RBLNConfig:
        if rbln_image_size is None:
            for processor in preprocessors:
                if hasattr(processor, "size"):
                    rbln_image_size = processor.size["shortest_edge"]
                    break
            if rbln_image_size is None:
                raise ValueError("`rbln_image_size` should be specified!")

        if rbln_batch_size is None:
            rbln_batch_size = 1

        input_info = [("pixel_values", [rbln_batch_size, 3, rbln_image_size, rbln_image_size], "float32")]

        rbln_runtime_config = RBLNRuntimeConfig(input_info=input_info)
        rbln_runtime_config.batch_size = rbln_batch_size
        meta = {"rbln_image_size": rbln_image_size}

        return RBLNConfig.from_rbln_runtime_configs([rbln_runtime_config], _rbln_meta=meta)


class RBLNModelForAudioClassification(RBLNModel):
    """
    This is a generic model class that will be instantiated as one of the model classes of the library (with a audio classification head) when created with the from_pretrained() class method
    This model inherits from [`RBLNModel`]. Check the superclass documentation for the generic methods the library implements for all its models.

    A class to convert and run pre-trained transformers based AudioClassification models on RBLN devices.
    It implements the methods to convert a pre-trained transformers AudioClassification model into a RBLN transformer model by:
    - transferring the checkpoint weights of the original into an optimized RBLN graph,
    - compiling the resulting graph using the RBLN compiler.

    Currently, this model class only supports the 'AST' model from the transformers library. Future updates may include support for additional model types.
    """

    model_type = "rbln_model"
    auto_model_class = AutoModelForAudioClassification

    @classmethod
    def _get_rbln_config(
        cls,
        preprocessors: "AutoFeatureExtractor",
        model_config: "PretrainedConfig",
        rbln_batch_size: Optional[int] = None,
        rbln_max_length: Optional[int] = None,
        rbln_num_mel_bins: Optional[int] = None,
    ) -> RBLNConfig:
        meta = {}

        if rbln_batch_size is None:
            rbln_batch_size = 1

        if rbln_num_mel_bins is None:
            rbln_num_mel_bins = getattr(model_config, "num_mel_bins", None)
            if rbln_num_mel_bins is None:
                for feature_extractor in preprocessors:
                    if hasattr(feature_extractor, "num_mel_bins"):
                        rbln_num_mel_bins = feature_extractor.num_mel_bins
                        break

        if rbln_num_mel_bins is None:
            raise ValueError("`rbln_num_mel_bins` should be specified!")

        if rbln_max_length is None:
            rbln_max_length = getattr(model_config, "max_length", None)
            for feature_extractor in preprocessors:
                if hasattr(feature_extractor, "max_length"):
                    rbln_max_length = feature_extractor.max_length
                    break

        if rbln_max_length is None:
            raise ValueError("`rbln_max_length` should be specified!")

        meta["rbln_batch_size"] = rbln_batch_size
        meta["rbln_max_length"] = rbln_max_length
        meta["rbln_num_mel_bins"] = rbln_num_mel_bins

        model_input_info = [
            ("input_values", [rbln_batch_size, rbln_max_length, rbln_num_mel_bins], "float32"),
        ]

        rbln_runtime_config = RBLNRuntimeConfig(input_info=model_input_info, batch_size=rbln_batch_size)

        rbln_config = RBLNConfig.from_rbln_runtime_configs(
            [rbln_runtime_config],
            _rbln_meta=meta,
        )

        return rbln_config
