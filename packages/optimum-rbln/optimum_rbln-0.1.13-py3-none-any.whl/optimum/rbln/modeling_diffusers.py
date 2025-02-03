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
import importlib
from os import PathLike
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

import torch

from .modeling_base import RBLNModel
from .modeling_config import ContextRblnConfig, use_rbln_config
from .utils.decorator_utils import remove_compile_time_kwargs


if TYPE_CHECKING:
    from diffusers.pipelines.controlnet.multicontrolnet import MultiControlNetModel


class RBLNDiffusionMixin:
    """
    RBLNDiffusionMixin provides essential functionalities for compiling Stable Diffusion pipeline components to run on RBLN NPUs.
    This mixin class serves as a base for implementing RBLN-compatible Stable Diffusion pipelines. It contains shared logic for
    handling the core components of Stable Diffusion.

    To use this mixin:

    1. Create a new pipeline class that inherits from both this mixin and the original StableDiffusionPipeline.
    2. Define the required _submodules class variable listing the components to be compiled.
    3. If needed, implement get_default_rbln_config for custom configuration of submodules.

    Example:
        ```python
        class RBLNStableDiffusionPipeline(RBLNDiffusionMixin, StableDiffusionPipeline):
            _submodules = ["text_encoder", "unet", "vae"]

            @classmethod
            def get_default_rbln_config(cls, model, submodule_name, rbln_config):
                # Configuration for other submodules...
                pass
        ```

    Class Variables:
        _submodules: List of submodule names that should be compiled (typically ["text_encoder", "unet", "vae"])

    Methods:
        from_pretrained: Creates and optionally compiles a model from a pretrained checkpoint

    Notes:
        - When `export=True`, all compatible submodules will be compiled for NPU inference
        - The compilation config can be customized per submodule by including submodule names
          as keys in rbln_config
    """

    _submodules = []

    @classmethod
    @property
    def use_encode(cls):
        return "Img2Img" in cls.__name__

    @classmethod
    def _get_unet_batch_size(cls, model: torch.nn.Module, rbln_config: Dict[str, Any]) -> int:
        # Calculates the batch size based on guidance scale
        batch_size = rbln_config.get("batch_size", 1)
        do_guidance = rbln_config.get("guidance_scale", 5.0) > 1.0 and model.unet.config.time_cond_proj_dim is None
        return batch_size * 2 if do_guidance else batch_size

    @classmethod
    def _get_vae_sample_size(cls, model: torch.nn.Module, rbln_config: Dict[str, Any]) -> Union[int, Tuple[int, int]]:
        image_size = (rbln_config.get("img_height"), rbln_config.get("img_width"))
        if (image_size[0] is None) != (image_size[1] is None):
            raise ValueError("Both image height and image width must be given or not given")
        elif image_size[0] is None and image_size[1] is None:
            if cls.use_encode:
                sample_size = model.vae.config.sample_size
            else:
                # In case of text2img, sample size of vae decoder is determined by unet.
                unet_sample_size = model.unet.config.sample_size
                if isinstance(unet_sample_size, int):
                    sample_size = unet_sample_size * model.vae_scale_factor
                else:
                    sample_size = (
                        unet_sample_size[0] * model.vae_scale_factor,
                        unet_sample_size[1] * model.vae_scale_factor,
                    )

        else:
            sample_size = (image_size[0], image_size[1])
        return sample_size

    @classmethod
    def _get_unet_sample_size(cls, model: torch.nn.Module, rbln_config: Dict[str, Any]) -> Union[int, Tuple[int, int]]:
        image_size = (rbln_config.get("img_height"), rbln_config.get("img_width"))
        if (image_size[0] is None) != (image_size[1] is None):
            raise ValueError("Both image height and image width must be given or not given")
        elif image_size[0] is None and image_size[1] is None:
            if cls.use_encode:
                # In case of img2img, sample size of unet is determined by vae encoder.
                vae_sample_size = model.vae.config.sample_size
                if isinstance(vae_sample_size, int):
                    sample_size = vae_sample_size // model.vae_scale_factor
                else:
                    sample_size = (
                        vae_sample_size[0] // model.vae_scale_factor,
                        vae_sample_size[1] // model.vae_scale_factor,
                    )
            else:
                sample_size = model.unet.config.sample_size
        else:
            sample_size = (image_size[0] // model.vae_scale_factor, image_size[1] // model.vae_scale_factor)
        return sample_size

    @classmethod
    def _get_default_config(cls, model: torch.nn.Module, rbln_config: Dict[str, Any]) -> Dict[str, Any]:
        # default configurations for each submodules
        return {"img2img_pipeline": cls.use_encode}

    @classmethod
    def get_default_rbln_config_text_encoder(
        cls, model: torch.nn.Module, rbln_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        batch_size = rbln_config.get("batch_size", 1)
        return {"batch_size": batch_size}

    @classmethod
    def get_default_rbln_config_text_encoder_2(
        cls, model: torch.nn.Module, rbln_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        batch_size = rbln_config.get("batch_size", 1)
        return {"batch_size": batch_size}

    @classmethod
    def get_default_rbln_config_unet(cls, model: torch.nn.Module, rbln_config: Dict[str, Any]) -> Dict[str, Any]:
        # configuration for unet
        unet_batch_size = cls._get_unet_batch_size(model, rbln_config)
        text_model_hidden_size = model.text_encoder_2.config.hidden_size if hasattr(model, "text_encoder_2") else None
        return {
            **cls._get_default_config(model, rbln_config),
            "max_seq_len": model.text_encoder.config.max_position_embeddings,
            "text_model_hidden_size": text_model_hidden_size,
            "batch_size": unet_batch_size,
            "sample_size": cls._get_unet_sample_size(model, rbln_config),
            "is_controlnet": "controlnet" in model.config.keys(),
        }

    @classmethod
    def get_default_rbln_config_vae(cls, model: torch.nn.Module, rbln_config: Dict[str, Any]) -> Dict[str, Any]:
        # configuration for vae
        batch_size = rbln_config.get("batch_size", 1)
        return {
            **cls._get_default_config(model, rbln_config),
            "sample_size": cls._get_vae_sample_size(model, rbln_config),
            "batch_size": batch_size,
        }

    @classmethod
    def get_default_rbln_config_controlnet(cls, model: torch.nn.Module, rbln_config: Dict[str, Any]) -> Dict[str, Any]:
        # configuration for controlnet
        unet_batch_size = cls._get_unet_batch_size(model, rbln_config)
        text_model_hidden_size = model.text_encoder_2.config.hidden_size if hasattr(model, "text_encoder_2") else None
        return {
            **cls._get_default_config(model, rbln_config),
            "max_seq_len": model.text_encoder.config.max_position_embeddings,
            "vae_sample_size": cls._get_vae_sample_size(model, rbln_config),
            "unet_sample_size": cls._get_unet_sample_size(model, rbln_config),
            "batch_size": unet_batch_size,
            "text_model_hidden_size": text_model_hidden_size,
        }

    @classmethod
    def get_default_rbln_config(
        cls, model: torch.nn.Module, submodule_name: str, rbln_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        # Returns the default configuration based on submodule name
        config_method = f"get_default_rbln_config_{submodule_name}"
        if hasattr(cls, config_method):
            return getattr(cls, config_method)(model, rbln_config)
        raise ValueError(f"Unknown submodule: {submodule_name}")

    @staticmethod
    def _maybe_apply_and_fuse_lora(
        model: torch.nn.Module,
        lora_ids: Optional[Union[str, List[str]]] = None,
        lora_weights_names: Optional[Union[str, List[str]]] = None,
        lora_scales: Optional[Union[float, List[float]]] = None,
    ) -> torch.nn.Module:
        lora_ids = [lora_ids] if isinstance(lora_ids, str) else lora_ids
        lora_weights_names = [lora_weights_names] if isinstance(lora_weights_names, str) else lora_weights_names
        lora_scales = [lora_scales] if isinstance(lora_scales, float) else lora_scales

        # adapt lora weight into pipeline before compilation
        if lora_ids and lora_weights_names:
            if len(lora_ids) == 1:
                if len(lora_ids) != len(lora_weights_names):
                    raise ValueError(
                        f"You must define the same number of lora ids ({len(lora_ids)} and lora weights ({len(lora_weights_names)}))"
                    )
                else:
                    model.load_lora_weights(lora_ids[0], weight_name=lora_weights_names[0])
                    model.fuse_lora(lora_scale=lora_scales[0] if lora_scales else 1.0)
            elif len(lora_ids) > 1:
                if not len(lora_ids) == len(lora_weights_names):
                    raise ValueError(
                        f"If you fuse {len(lora_ids)} lora models, but you must define the same number for lora weights and adapters."
                    )

                adapter_names = [f"adapter_{i}" for i in range(len(lora_ids))]

                for lora_id, lora_weight, adapter_name in zip(lora_ids, lora_weights_names, adapter_names):
                    model.load_lora_weights(lora_id, weight_name=lora_weight, adapter_name=adapter_name)

                if lora_scales:
                    model.set_adapters(adapter_names, adapter_weights=lora_scales)

                model.fuse_lora()
        return model

    @classmethod
    @use_rbln_config
    def from_pretrained(
        cls,
        model_id: str,
        *,
        export: bool = False,
        model_save_dir: Optional[PathLike] = None,
        rbln_config: Dict[str, Any] = {},
        lora_ids: Optional[Union[str, List[str]]] = None,
        lora_weights_names: Optional[Union[str, List[str]]] = None,
        lora_scales: Optional[Union[float, List[float]]] = None,
        **kwargs,
    ) -> RBLNModel:
        if export:
            # keep submodules if user passed any of them.
            passed_submodules = {
                name: kwargs.pop(name) for name in cls._submodules if isinstance(kwargs.get(name), RBLNModel)
            }

        else:
            # raise error if any of submodules are torch module.
            for name in cls._submodules:
                if isinstance(kwargs.get(name), torch.nn.Module):
                    raise AssertionError(
                        f"{name} is not compiled torch module. If you want to compile, set `export=True`."
                    )

        with ContextRblnConfig(
            device=rbln_config.get("device"),
            device_map=rbln_config.get("device_map"),
            create_runtimes=rbln_config.get("create_runtimes"),
            optimize_host_mem=rbln_config.get("optimize_host_memory"),
        ):
            model = super().from_pretrained(pretrained_model_name_or_path=model_id, **kwargs)

        if not export:
            return model

        model = cls._maybe_apply_and_fuse_lora(
            model,
            lora_ids=lora_ids,
            lora_weights_names=lora_weights_names,
            lora_scales=lora_scales,
        )

        compiled_submodules = cls._compile_submodules(model, passed_submodules, model_save_dir, rbln_config)
        return cls._construct_pipe(model, compiled_submodules, model_save_dir, rbln_config)

    @classmethod
    def _compile_submodules(
        cls,
        model: torch.nn.Module,
        passed_submodules: Dict[str, RBLNModel],
        model_save_dir: Optional[PathLike],
        rbln_config: Dict[str, Any],
    ) -> Dict[str, RBLNModel]:
        # Compile submodules based on rbln_config
        compiled_submodules = {}

        # FIXME : Currently, optimum-rbln for transformer does not use base rbln config.
        base_rbln_config = {k: v for k, v in rbln_config.items() if k not in cls._submodules}
        for submodule_name in cls._submodules:
            submodule = passed_submodules.get(submodule_name) or getattr(model, submodule_name, None)
            submodule_rbln_config = cls.get_default_rbln_config(model, submodule_name, rbln_config)
            submodule_rbln_config.update(base_rbln_config)
            submodule_rbln_config.update(rbln_config.get(submodule_name, {}))

            if submodule is None:
                raise ValueError(f"submodule ({submodule_name}) cannot be accessed since it is not provided.")
            elif isinstance(submodule, RBLNModel):
                pass
            elif submodule_name == "controlnet" and hasattr(submodule, "nets"):
                # In case of multicontrolnet
                submodule = cls._compile_multicontrolnet(
                    controlnets=submodule,
                    model_save_dir=model_save_dir,
                    controlnet_rbln_config=submodule_rbln_config,
                )
            elif isinstance(submodule, torch.nn.Module):
                submodule_cls: RBLNModel = getattr(
                    importlib.import_module("optimum.rbln"), f"RBLN{submodule.__class__.__name__}"
                )
                submodule = submodule_cls.from_model(
                    model=submodule,
                    subfolder=submodule_name,
                    model_save_dir=model_save_dir,
                    rbln_config=submodule_rbln_config,
                )
            else:
                raise ValueError(f"Unknown class of submodule({submodule_name}) : {submodule.__class__.__name__} ")

            compiled_submodules[submodule_name] = submodule
        return compiled_submodules

    @classmethod
    def _compile_multicontrolnet(
        cls,
        controlnets: "MultiControlNetModel",
        model_save_dir: Optional[PathLike],
        controlnet_rbln_config: Dict[str, Any],
    ):
        # Compile multiple ControlNet models for a MultiControlNet setup
        from .diffusers.models.controlnet import RBLNControlNetModel
        from .diffusers.pipelines.controlnet import RBLNMultiControlNetModel

        compiled_controlnets = [
            RBLNControlNetModel.from_model(
                model=controlnet,
                subfolder="controlnet" if i == 0 else f"controlnet_{i}",
                model_save_dir=model_save_dir,
                rbln_config=controlnet_rbln_config,
            )
            for i, controlnet in enumerate(controlnets.nets)
        ]
        return RBLNMultiControlNetModel(compiled_controlnets, config=controlnets.nets[0].config)

    @classmethod
    def _construct_pipe(cls, model, submodules, model_save_dir, rbln_config):
        # Construct finalize pipe setup with compiled submodules and configurations

        if model_save_dir is not None:
            # To skip saving original pytorch modules
            for submodule_name in cls._submodules:
                delattr(model, submodule_name)

            # Direct calling of `save_pretrained` causes config.unet = (None, None).
            # So config must be saved again, later.
            model.save_pretrained(model_save_dir)
            # FIXME: Here, model touches its submodules such as model.unet,
            # Causing warning messeages.

        update_dict = {}
        for submodule_name in cls._submodules:
            # replace submodule
            setattr(model, submodule_name, submodules[submodule_name])
            update_dict[submodule_name] = ("optimum.rbln", submodules[submodule_name].__class__.__name__)

        # Update config to be able to load from model directory.
        #
        # e.g)
        # update_dict = {
        #     "vae": ("optimum.rbln", "RBLNAutoencoderKL"),
        #     "text_encoder": ("optimum.rbln", "RBLNCLIPTextModel"),
        #     "unet": ("optimum.rbln", "RBLNUNet2DConditionModel"),
        # }
        model.register_to_config(**update_dict)

        if model_save_dir:
            # overwrite to replace incorrect config
            model.save_config(model_save_dir)

        if rbln_config.get("optimize_host_memory") is False:
            # Keep compiled_model objs to further analysis. -> TODO: remove soon...
            model.compiled_models = []
            for name in cls._submodules:
                submodule = getattr(model, name)
                model.compiled_models.extend(submodule.compiled_models)

        return model

    @remove_compile_time_kwargs
    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)
