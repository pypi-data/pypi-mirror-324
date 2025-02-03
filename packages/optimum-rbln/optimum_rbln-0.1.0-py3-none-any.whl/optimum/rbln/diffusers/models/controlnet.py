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
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Union

import rebel
import torch
from diffusers import ControlNetModel
from optimum.exporters import TasksManager
from transformers import AutoConfig, AutoModel, PretrainedConfig

from ...modeling_base import RBLNModel
from ...modeling_config import RBLNConfig, RBLNRuntimeConfig


logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from transformers import AutoFeatureExtractor, AutoProcessor, AutoTokenizer


class _ControlNetModel(torch.nn.Module):
    def __init__(self, controlnet: "ControlNetModel"):
        super().__init__()
        self.controlnet = controlnet

    def forward(
        self,
        sample: torch.Tensor,
        timestep: torch.Tensor,
        encoder_hidden_states: torch.Tensor,
        controlnet_cond: torch.Tensor,
        conditioning_scale,
    ):
        down_block_res_samples, mid_block_res_sample = self.controlnet(
            sample=sample,
            timestep=timestep,
            encoder_hidden_states=encoder_hidden_states,
            controlnet_cond=controlnet_cond,
            conditioning_scale=conditioning_scale,
            return_dict=False,
        )
        return down_block_res_samples, mid_block_res_sample


class RBLNControlNetModel(RBLNModel):
    model_type = "rbln_model"
    auto_model_class = AutoModel  # feature extraction

    def __post_init__(self, **kwargs):
        self.dtype = torch.float32

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        def get_model_from_task(
            task: str,
            model_name_or_path: Union[str, Path],
            **kwargs,
        ):
            return ControlNetModel.from_pretrained(pretrained_model_name_or_path=model_name_or_path, **kwargs)

        tasktmp = TasksManager.get_model_from_task
        configtmp = AutoConfig.from_pretrained
        modeltmp = AutoModel.from_pretrained
        TasksManager.get_model_from_task = get_model_from_task
        AutoConfig.from_pretrained = ControlNetModel.load_config
        AutoModel.from_pretrained = ControlNetModel.from_pretrained
        rt = super().from_pretrained(*args, **kwargs)
        AutoConfig.from_pretrained = configtmp
        AutoModel.from_pretrained = modeltmp
        TasksManager.get_model_from_task = tasktmp
        return rt

    @classmethod
    def compile(cls, model, rbln_runtime_config: Optional[RBLNRuntimeConfig] = None):
        compiled_model = rebel.compile_from_torch(
            _ControlNetModel(model),
            input_info=rbln_runtime_config.input_info,
            batch_size=rbln_runtime_config.batch_size,
            fusion=rbln_runtime_config.fusion,
        )
        return compiled_model

    @classmethod
    def _get_rbln_config(
        cls,
        preprocessors: Union["AutoFeatureExtractor", "AutoProcessor", "AutoTokenizer"],
        model_config: "PretrainedConfig",
        rbln_max_seq_len: Optional[int] = None,
        rbln_batch_size: Optional[int] = None,
        rbln_img_width: Optional[int] = None,
        rbln_img_height: Optional[int] = None,
        rbln_vae_scale_factor: Optional[int] = None,
    ) -> RBLNConfig:
        meta = {"type": "controlnet"}

        if rbln_batch_size is None:
            rbln_batch_size = 1

        if rbln_max_seq_len is None:
            rbln_max_seq_len = 77

        input_width = rbln_img_width // rbln_vae_scale_factor
        input_height = rbln_img_height // rbln_vae_scale_factor

        rbln_runtime_config = RBLNRuntimeConfig(
            input_info=[
                (
                    "sample",
                    [
                        rbln_batch_size,
                        model_config.in_channels,
                        input_width,
                        input_height,
                    ],
                    "float32",
                ),
                ("timestep", [], "float32"),
                (
                    "encoder_hidden_states",
                    [
                        rbln_batch_size,
                        rbln_max_seq_len,
                        model_config.cross_attention_dim,
                    ],
                    "float32",
                ),
                ("controlnet_cond", [rbln_batch_size, 3, rbln_img_width, rbln_img_height], "float32"),
                ("conditioning_scale", [], "float32"),
            ],
            batch_size=rbln_batch_size,
        )
        rbln_config = RBLNConfig.from_rbln_runtime_configs([rbln_runtime_config], _rbln_meta=meta)
        return rbln_config

    def forward(
        self,
        sample: torch.FloatTensor,
        timestep: Union[torch.Tensor, float, int],
        encoder_hidden_states: torch.Tensor,
        controlnet_cond: torch.FloatTensor,
        conditioning_scale: torch.Tensor = 1.0,
        **kwargs,
    ):
        """
        The [`ControlNetModel`] forward method.
        """
        output = super().forward(
            sample.contiguous(),
            timestep.float(),
            encoder_hidden_states,
            controlnet_cond,
            torch.tensor(conditioning_scale),
        )
        down_block_res_samples = output[:-1]
        mid_block_res_sample = output[-1]

        return down_block_res_samples, mid_block_res_sample
