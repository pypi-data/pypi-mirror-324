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
import inspect
import logging
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

import rebel
import torch
import transformers
from huggingface_hub.constants import HUGGINGFACE_HUB_CACHE
from transformers import (
    AutoConfig,
    AutoModelForAudioClassification,
    AutoModelForImageClassification,
    AutoModelForMaskedLM,
    AutoModelForQuestionAnswering,
    AutoModelForSequenceClassification,
    PretrainedConfig,
)

from .modeling_base import RBLNBaseModel
from .modeling_config import DEFAULT_COMPILED_MODEL_NAME, RBLNCompileConfig, RBLNConfig, use_rbln_config


if TYPE_CHECKING:
    from transformers import (
        AutoFeatureExtractor,
        AutoProcessor,
        AutoTokenizer,
        PreTrainedModel,
    )

logger = logging.getLogger(__name__)


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
    def save_torch_artifacts(
        cls,
        model: "PreTrainedModel",
        save_dir_path: Path,
        subfolder: str,
        rbln_config: RBLNConfig,
    ):
        """
        If you are unavoidably running on a CPU rather than an RBLN device,
        store the torch tensor, weight, etc. in this function.
        """

    @classmethod
    def wrap_model_if_needed(cls, model: torch.nn.Module, rbln_config: RBLNConfig) -> torch.nn.Module:
        # Wrap the model if needed.
        return model

    @classmethod
    def get_compiled_model(cls, model: "PreTrainedModel", rbln_config: RBLNConfig):
        model = cls.wrap_model_if_needed(model, rbln_config)
        rbln_compile_config = rbln_config.compile_cfgs[0]
        compiled_model = cls.compile(model, rbln_compile_config=rbln_compile_config)
        return compiled_model

    @classmethod
    @use_rbln_config
    def from_model(
        cls,
        model: "PreTrainedModel",
        config: Optional[PretrainedConfig] = None,
        rbln_config: Dict[str, Any] = {},
        model_save_dir: Optional[Union[str, Path, TemporaryDirectory]] = None,
        subfolder: str = "",
        **kwargs,
    ):
        preprocessors = kwargs.pop("preprocessors", [])
        rbln_kwargs = rbln_config

        # Directory to save compile artifacts(.rbln) and original configs
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

        # Save configs
        if config is None:
            config = model.config
            # remote_config
            if hasattr(config, "auto_map") and "AutoConfig" in config.auto_map:
                config = AutoConfig.from_pretrained(config._name_or_path, **kwargs)

        if hasattr(model, "can_generate") and model.can_generate():
            generation_config = model.generation_config
            generation_config.save_pretrained(save_dir_path / subfolder)

        if not isinstance(config, PretrainedConfig):  # diffusers config
            config = PretrainedConfig(**config)
        config.save_pretrained(save_dir_path / subfolder)

        # Save preprocessor
        for preprocessor in preprocessors:
            preprocessor.save_pretrained(save_dir_path / subfolder)

        # Get compilation arguments (e.g. input_info)
        rbln_config: RBLNConfig = cls.get_rbln_config(
            preprocessors=preprocessors, model_config=config, rbln_kwargs=rbln_kwargs
        )
        # rbln_config.update_runtime_cfg(rbln_kwargs) # This is done in get_rbln_config

        compiled_model: Union[rebel.RBLNCompiledModel, Dict[str, rebel.RBLNCompiledModel]] = cls.get_compiled_model(
            model, rbln_config=rbln_config
        )

        # Save compiled models (.rbln)
        (save_dir_path / subfolder).mkdir(exist_ok=True)
        if not isinstance(compiled_model, dict):
            compiled_models = {DEFAULT_COMPILED_MODEL_NAME: compiled_model}
        else:
            compiled_models = compiled_model
        for compiled_model_name, cm in compiled_models.items():
            cm.save(save_dir_path / subfolder / f"{compiled_model_name}.rbln")
        rbln_config.save(save_dir_path / subfolder)

        # Save torch artifacts (e.g. embedding matrix if needed.)
        cls.save_torch_artifacts(model, save_dir_path=save_dir_path, subfolder=subfolder, rbln_config=rbln_config)

        # Load submodules
        if len(cls._rbln_submodules) > 0:
            rbln_submodules = cls._load_submodules(
                model=model,
                model_save_dir=save_dir,
                rbln_kwargs=rbln_kwargs,
                **kwargs,
            )
        else:
            rbln_submodules = []

        # Instantiate
        return cls._from_pretrained(
            model_id=save_dir_path,
            config=config,
            model_save_dir=save_dir,
            subfolder=subfolder,
            rbln_config=rbln_config,
            rbln_compiled_models=compiled_models,
            rbln_submodules=rbln_submodules,
            **kwargs,
        )

    @classmethod
    def get_pytorch_model(
        cls,
        model_id: str,
        use_auth_token: Optional[Union[bool, str]] = None,
        revision: Optional[str] = None,
        force_download: bool = False,
        cache_dir: Optional[str] = HUGGINGFACE_HUB_CACHE,
        subfolder: str = "",
        local_files_only: bool = False,
        trust_remote_code: bool = False,
        # Some rbln-kwargs should be applied before loading torch module (i.e. quantized llm)
        rbln_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> "PreTrainedModel":
        kwargs = cls.update_kwargs(kwargs)
        return cls.hf_class.from_pretrained(
            model_id,
            subfolder=subfolder,
            revision=revision,
            cache_dir=cache_dir,
            use_auth_token=use_auth_token,
            local_files_only=local_files_only,
            force_download=force_download,
            trust_remote_code=trust_remote_code,
            **kwargs,
        )

    @classmethod
    def _create_runtimes(
        cls,
        compiled_models: List[rebel.RBLNCompiledModel],
        rbln_device_map: Dict[str, int],
    ) -> List[rebel.Runtime]:
        device = rbln_device_map[DEFAULT_COMPILED_MODEL_NAME]
        return [compiled_model.create_runtime(tensor_type="pt", device=device) for compiled_model in compiled_models]

    def forward(self, *args: List[torch.Tensor], **kwargs: Dict[str, torch.Tensor]):
        output = self.model[0](*args, **kwargs)
        return output


class RBLNModelForQuestionAnswering(RBLNModel):
    auto_model_class = AutoModelForQuestionAnswering
    rbln_model_input_names = ["input_ids", "attention_mask", "token_type_ids"]

    @classmethod
    def _get_rbln_config(
        cls,
        preprocessors: Optional[Union["AutoFeatureExtractor", "AutoProcessor", "AutoTokenizer"]],
        model_config: Optional["PretrainedConfig"] = None,
        rbln_kwargs: Dict[str, Any] = {},
    ) -> RBLNConfig:
        rbln_max_seq_len = rbln_kwargs.get("max_seq_len", None)
        rbln_batch_size = rbln_kwargs.get("batch_size", None)
        rbln_model_input_names = rbln_kwargs.get("model_input_names", None)

        if rbln_max_seq_len is None:
            for tokenizer in preprocessors:
                if hasattr(tokenizer, "model_max_length"):
                    rbln_max_seq_len = tokenizer.model_max_length
                    break
            if rbln_max_seq_len is None:
                raise ValueError("`rbln_max_seq_len` should be specified!")

        if rbln_batch_size is None:
            rbln_batch_size = 1

        if rbln_model_input_names is None:
            for tokenizer in preprocessors:
                if hasattr(tokenizer, "model_input_names"):
                    rbln_model_input_names = tokenizer.model_input_names
                    break
            if rbln_model_input_names is None and hasattr(cls, "rbln_model_input_names"):
                rbln_model_input_names = cls.rbln_model_input_names
            elif rbln_model_input_names is None and hasattr(cls, "rbln_model_input_names") is False:
                input_names_order = inspect.signature(cls.hf_class.forward).parameters.keys()
                raise ValueError(
                    "Specify the model input names obtained by the tokenizer via `rbln_model_input_names`, "
                    f"and be sure to make the order of the inputs same as QuestionAnswering forward() arguments like ({list(input_names_order)})"
                )

        input_info = [
            (model_input_name, [rbln_batch_size, rbln_max_seq_len], "int64")
            for model_input_name in rbln_model_input_names
        ]

        rbln_compile_config = RBLNCompileConfig(input_info=input_info)
        rbln_config = RBLNConfig(
            rbln_cls=cls.__name__,
            compile_cfgs=[rbln_compile_config],
            rbln_kwargs=rbln_kwargs,
        )
        rbln_config.model_cfg.update({"max_seq_len": rbln_max_seq_len})
        return rbln_config


class RBLNModelForImageClassification(RBLNModel):
    """
    This is a generic model class that will be instantiated as one of the model classes of the library (with a image classification head) when created with the from_pretrained() class method
    """

    auto_model_class = AutoModelForImageClassification

    @classmethod
    def _get_rbln_config(
        cls,
        preprocessors: Optional[Union["AutoFeatureExtractor", "AutoProcessor", "AutoTokenizer"]],
        model_config: Optional["PretrainedConfig"] = None,
        rbln_kwargs: Dict[str, Any] = {},
    ) -> RBLNConfig:
        rbln_image_size = rbln_kwargs.get("image_size", None)
        rbln_batch_size = rbln_kwargs.get("batch_size", None)

        if rbln_image_size is None:
            for processor in preprocessors:
                if hasattr(processor, "size"):
                    if all(required_key in processor.size.keys() for required_key in ["height", "width"]):
                        rbln_image_size = (processor.size["height"], processor.size["width"])
                    elif "shortest_edge" in processor.size.keys():
                        rbln_image_size = (processor.size["shortest_edge"], processor.size["shortest_edge"])
                    elif "longest_edge" in processor.size.keys():
                        rbln_image_size = (processor.size["longest_edge"], processor.size["longest_edge"])
                    break

            if rbln_image_size is None:
                rbln_image_size = model_config.image_size

            if rbln_image_size is None:
                raise ValueError("`rbln_image_size` should be specified!")

        if rbln_batch_size is None:
            rbln_batch_size = 1

        if isinstance(rbln_image_size, int):
            rbln_image_height, rbln_image_width = rbln_image_size, rbln_image_size
        elif isinstance(rbln_image_size, (list, tuple)):
            rbln_image_height, rbln_image_width = rbln_image_size[0], rbln_image_size[1]
        elif isinstance(rbln_image_size, dict):
            rbln_image_height, rbln_image_width = rbln_image_size["height"], rbln_image_size["width"]
        else:
            raise ValueError(
                "`rbln_image_size` should be `int` (ex. 224), `tuple` (ex. 224, 224), `dict` (ex. {'height': 224, 'width': 224}) format"
            )

        input_info = [
            (
                "pixel_values",
                [rbln_batch_size, 3, rbln_image_height, rbln_image_width],
                "float32",
            )
        ]

        rbln_compile_config = RBLNCompileConfig(input_info=input_info)
        return RBLNConfig(rbln_cls=cls.__name__, compile_cfgs=[rbln_compile_config], rbln_kwargs=rbln_kwargs)


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

    auto_model_class = AutoModelForAudioClassification

    @classmethod
    def _get_rbln_config(
        cls,
        preprocessors: "AutoFeatureExtractor",
        model_config: "PretrainedConfig",
        rbln_kwargs: Dict[str, Any] = {},
    ) -> RBLNConfig:
        rbln_batch_size = rbln_kwargs.get("batch_size", None)
        rbln_max_length = rbln_kwargs.get("max_length", None)
        rbln_num_mel_bins = rbln_kwargs.get("num_mel_bins", None)

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

        input_info = [
            (
                "input_values",
                [rbln_batch_size, rbln_max_length, rbln_num_mel_bins],
                "float32",
            ),
        ]

        rbln_compile_config = RBLNCompileConfig(input_info=input_info)
        rbln_config = RBLNConfig(
            rbln_cls=cls.__name__,
            compile_cfgs=[rbln_compile_config],
            rbln_kwargs=rbln_kwargs,
        )
        rbln_config.model_cfg.update(
            {
                "batch_size": rbln_batch_size,
                "max_length": rbln_max_length,
                "num_mel_bins": rbln_num_mel_bins,
            }
        )
        return rbln_config


class RBLNModelForSequenceClassification(RBLNModel):
    """
    This is a generic model class that will be instantiated as one of the model classes of the library (with a sequence classification head) when created with the from_pretrained() class method
    This model inherits from [`RBLNModel`]. Check the superclass documentation for the generic methods the library implements for all its models.

    A class to convert and run pre-trained transformers based SequenceClassification models on RBLN devices.
    It implements the methods to convert a pre-trained transformers SequenceClassification model into a RBLN transformer model by:
    - transferring the checkpoint weights of the original into an optimized RBLN graph,
    - compiling the resulting graph using the RBLN compiler.

    Currently, this model class supports the 'XLMRoberta' and 'Roberta' model from the transformers library. Future updates may include support for additional model types.
    """

    auto_model_class = AutoModelForSequenceClassification

    @classmethod
    def _get_rbln_config(
        cls,
        preprocessors: Optional[Union["AutoFeatureExtractor", "AutoProcessor", "AutoTokenizer"]],
        model_config: Optional["PretrainedConfig"] = None,
        rbln_kwargs: Dict[str, Any] = {},
    ) -> RBLNConfig:
        rbln_max_seq_len = rbln_kwargs.get("max_seq_len", None)
        rbln_model_input_names = rbln_kwargs.get("model_input_names", None)
        rbln_batch_size = rbln_kwargs.get("batch_size", None)

        max_position_embeddings = getattr(model_config, "n_positions", None) or getattr(
            model_config, "max_position_embeddings", None
        )

        if rbln_max_seq_len is None:
            rbln_max_seq_len = max_position_embeddings
            if rbln_max_seq_len is None:
                for tokenizer in preprocessors:
                    if hasattr(tokenizer, "model_max_length"):
                        rbln_max_seq_len = tokenizer.model_max_length
                        break
                if rbln_max_seq_len is None:
                    raise ValueError("`rbln_max_seq_len` should be specified!")

        if max_position_embeddings is not None and rbln_max_seq_len > max_position_embeddings:
            raise ValueError("`rbln_enc_max_seq_len` should be less or equal than max_position_embeddings!")

        if rbln_model_input_names is None:
            for tokenizer in preprocessors:
                if hasattr(tokenizer, "model_input_names"):
                    rbln_model_input_names = tokenizer.model_input_names
                    break
            if rbln_model_input_names is None and hasattr(cls, "rbln_model_input_names"):
                rbln_model_input_names = cls.rbln_model_input_names
            elif rbln_model_input_names is None and hasattr(cls, "rbln_model_input_names") is False:
                original_model_class = getattr(transformers, model_config.architectures[0])
                input_names_order = inspect.signature(original_model_class.forward).parameters.keys()
                raise ValueError(
                    "Specify the model input names obtained by the tokenizer via `rbln_model_input_names`, "
                    f"and be sure to make the order of the inputs same as SequenceClassification forward() arguments like ({list(input_names_order)})"
                )

        if rbln_batch_size is None:
            rbln_batch_size = 1

        input_info = [
            (model_input_name, [rbln_batch_size, rbln_max_seq_len], "int64")
            for model_input_name in rbln_model_input_names
        ]

        rbln_compile_config = RBLNCompileConfig(input_info=input_info)
        rbln_config = RBLNConfig(
            rbln_cls=cls.__name__,
            compile_cfgs=[rbln_compile_config],
            rbln_kwargs=rbln_kwargs,
        )
        rbln_config.model_cfg.update({"max_seq_len": rbln_max_seq_len})
        return rbln_config


class RBLNModelForMaskedLM(RBLNModel):
    auto_model_class = AutoModelForMaskedLM

    @classmethod
    def _get_rbln_config(
        cls,
        preprocessors: Optional[Union["AutoFeatureExtractor", "AutoProcessor", "AutoTokenizer"]],
        model_config: Optional["PretrainedConfig"] = None,
        rbln_kwargs: Dict[str, Any] = {},
    ) -> RBLNConfig:
        rbln_max_seq_len = rbln_kwargs.get("max_seq_len", None)
        rbln_model_input_names = rbln_kwargs.get("model_input_names", None)
        rbln_batch_size = rbln_kwargs.get("batch_size", None)

        max_position_embeddings = getattr(model_config, "n_positions", None) or getattr(
            model_config, "max_position_embeddings", None
        )

        if rbln_max_seq_len is None:
            rbln_max_seq_len = max_position_embeddings
            if rbln_max_seq_len is None:
                for tokenizer in preprocessors:
                    if hasattr(tokenizer, "model_max_length"):
                        rbln_max_seq_len = tokenizer.model_max_length
                        break
                if rbln_max_seq_len is None:
                    raise ValueError("`rbln_max_seq_len` should be specified!")

        if max_position_embeddings is not None and rbln_max_seq_len > max_position_embeddings:
            raise ValueError("`rbln_enc_max_seq_len` should be less or equal than max_position_embeddings!")

        if rbln_model_input_names is None:
            for tokenizer in preprocessors:
                if hasattr(tokenizer, "model_input_names"):
                    rbln_model_input_names = tokenizer.model_input_names
                    break
            if rbln_model_input_names is None and hasattr(cls, "rbln_model_input_names"):
                rbln_model_input_names = cls.rbln_model_input_names
            elif rbln_model_input_names is None and hasattr(cls, "rbln_model_input_names") is False:
                input_names_order = inspect.signature(cls.hf_class.forward).parameters.keys()
                raise ValueError(
                    "Specify the model input names obtained by the tokenizer via `rbln_model_input_names`, "
                    f"and be sure to make the order of the inputs same as MaskedLM forward() arguments like ({list(input_names_order)})"
                )

        if rbln_batch_size is None:
            rbln_batch_size = 1

        input_info = [
            (model_input_name, [rbln_batch_size, rbln_max_seq_len], "int64")
            for model_input_name in rbln_model_input_names
        ]

        rbln_compile_config = RBLNCompileConfig(input_info=input_info)
        rbln_config = RBLNConfig(
            rbln_cls=cls.__name__,
            compile_cfgs=[rbln_compile_config],
            rbln_kwargs=rbln_kwargs,
        )
        rbln_config.model_cfg.update({"max_seq_len": rbln_max_seq_len})
        return rbln_config
