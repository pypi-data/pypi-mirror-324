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
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

import rebel
import torch
from diffusers import ControlNetModel
from diffusers.pipelines.controlnet.multicontrolnet import MultiControlNetModel
from optimum.exporters import TasksManager
from transformers import AutoConfig, AutoModel, PretrainedConfig, PreTrainedModel

from ....modeling_base import RBLNBaseModel
from ....modeling_config import RBLNConfig
from ...models.controlnet import RBLNControlNetModel


logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from transformers import (
        PretrainedConfig,
        PreTrainedModel,
    )


class RBLNMultiControlNetModel(RBLNBaseModel):
    model_type = "rbln_model"
    auto_model_class = AutoModel

    def __init__(
        self,
        models: List[Union[PreTrainedModel, rebel.RBLNCompiledModel]],
        config: PretrainedConfig = None,
        preprocessors: Optional[List] = None,
        rbln_config: Optional[RBLNConfig] = None,
        **kwargs,
    ):
        super().__init__(
            models,
            config,
            preprocessors,
            rbln_config,
            **kwargs,
        )

        if not isinstance(config, PretrainedConfig):
            config = PretrainedConfig(**config)

        for i in range(len(models)):
            self.runtimes[i].config = config
        self.nets = self.runtimes
        self.dtype = torch.float32

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        def get_model_from_task(
            task: str,
            model_name_or_path: Union[str, Path],
            **kwargs,
        ):
            return MultiControlNetModel.from_pretrained(pretrained_model_path=model_name_or_path, **kwargs)

        tasktmp = TasksManager.get_model_from_task
        configtmp = AutoConfig.from_pretrained
        modeltmp = AutoModel.from_pretrained
        TasksManager.get_model_from_task = get_model_from_task
        AutoConfig.from_pretrained = ControlNetModel.load_config
        AutoModel.from_pretrained = MultiControlNetModel.from_pretrained
        rt = super().from_pretrained(*args, **kwargs)
        AutoConfig.from_pretrained = configtmp
        AutoModel.from_pretrained = modeltmp
        TasksManager.get_model_from_task = tasktmp
        return rt

    @classmethod
    def _from_pretrained(
        cls,
        model_id: Union[str, Path],
        config: "PretrainedConfig",
        use_auth_token: Optional[Union[bool, str]] = None,
        revision: Optional[str] = None,
        force_download: bool = False,
        cache_dir: Optional[str] = None,
        file_name: Optional[str] = None,
        subfolder: str = "",
        local_files_only: bool = False,
        **kwargs,
    ) -> RBLNBaseModel:

        if isinstance(model_id, str):
            model_path = Path(model_id)
        else:
            model_path = model_id / "controlnet"

        rbln_files = []
        rbln_config_filenames = []
        idx = 0
        model_load_path = model_path

        while model_load_path.is_dir():
            rbln_files.append(list(model_load_path.glob("**/*.rbln"))[0])
            rbln_config_filenames.append(model_load_path)
            idx += 1
            model_load_path = Path(str(model_path) + f"_{idx}")

        if len(rbln_files) == 0:
            raise FileNotFoundError(f"Could not find any rbln model file in {model_path}")

        if len(rbln_config_filenames) == 0:
            raise FileNotFoundError(f"Could not find `rbln_config.json` file in {model_path}")

        models = []
        for rconf, rfiles in zip(rbln_config_filenames, rbln_files):
            rbln_config = RBLNConfig.load(str(rconf))
            models.append(rebel.RBLNCompiledModel(rfiles))

        preprocessors = []

        return cls(
            models,
            config,
            preprocessors,
            rbln_config=rbln_config,
            **kwargs,
        )

    def _save_pretrained(self, save_directory: Union[str, Path]):
        idx = 0
        real_save_dir_path = save_directory
        for compiled_model in self.compiled_models:
            dst_path = Path(real_save_dir_path) / "compiled_model.rbln"
            if not os.path.exists(real_save_dir_path):
                os.makedirs(real_save_dir_path)
            compiled_model.save(dst_path)
            self.rbln_config.save(real_save_dir_path)
            idx += 1
            real_save_dir_path = save_directory + f"_{idx}"

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
        **kwargs,
    ) -> "RBLNMultiControlNetModel":

        task = kwargs.pop("task", None)
        if task is None:
            task = TasksManager.infer_task_from_model(cls.auto_model_class)

        save_dir = TemporaryDirectory()
        save_dir_path = Path(save_dir.name)

        rbln_config_kwargs, rbln_constructor_kwargs = cls.pop_rbln_kwargs_from_kwargs(kwargs)
        img_width = rbln_config_kwargs.pop("rbln_img_width", None)
        img_height = rbln_config_kwargs.pop("rbln_img_height", None)
        vae_scale_factor = rbln_config_kwargs.pop("rbln_vae_scale_factor", None)
        batch_size = rbln_config_kwargs.pop("rbln_batch_size", None)

        model: MultiControlNetModel = TasksManager.get_model_from_task(
            task=task,
            model_name_or_path=model_id,
        )

        model_path_to_load = model_id
        real_save_dir_path = save_dir_path / "controlnet"

        for idx in range(len(model.nets)):
            suffix = "" if idx == 0 else f"_{idx}"
            controlnet = RBLNControlNetModel.from_pretrained(
                model_path_to_load + suffix,
                export=True,
                rbln_batch_size=batch_size,
                rbln_img_width=img_width,
                rbln_img_height=img_height,
                rbln_vae_scale_factor=vae_scale_factor,
            )
            controlnet.save_pretrained(real_save_dir_path)
            real_save_dir_path = save_dir_path / f"controlnet_{idx+1}"

        return cls._from_pretrained(
            model_id=save_dir_path,
            config=config,
            model_save_dir=save_dir,
            **rbln_constructor_kwargs,
            **kwargs,
        )

    def _create_runtimes(self, rbln_device_map: Dict[str, int]) -> List[rebel.Runtime]:
        device_val = rbln_device_map["compiled_model"]

        return [
            compiled_model.create_runtime(tensor_type="pt", device=device_val)
            for compiled_model in self.compiled_models
        ]

    def forward(
        self,
        sample: torch.FloatTensor,
        timestep: Union[torch.Tensor, float, int],
        encoder_hidden_states: torch.Tensor,
        controlnet_cond: List[torch.tensor],
        conditioning_scale: List[float],
        class_labels: Optional[torch.Tensor] = None,
        timestep_cond: Optional[torch.Tensor] = None,
        attention_mask: Optional[torch.Tensor] = None,
        added_cond_kwargs: Optional[Dict[str, torch.Tensor]] = None,
        cross_attention_kwargs: Optional[Dict[str, Any]] = None,
        guess_mode: bool = False,
        return_dict: bool = True,
    ):
        for i, (image, scale, controlnet) in enumerate(zip(controlnet_cond, conditioning_scale, self.nets)):
            output = controlnet(
                sample=sample.contiguous(),
                timestep=timestep,
                encoder_hidden_states=encoder_hidden_states,
                controlnet_cond=image,
                conditioning_scale=torch.tensor(scale),
            )

            down_samples, mid_sample = output[:-1], output[-1]

            # merge samples
            if i == 0:
                down_block_res_samples, mid_block_res_sample = down_samples, mid_sample
            else:
                down_block_res_samples = [
                    samples_prev + samples_curr
                    for samples_prev, samples_curr in zip(down_block_res_samples, down_samples)
                ]
                mid_block_res_sample += mid_sample

        return down_block_res_samples, mid_block_res_sample
