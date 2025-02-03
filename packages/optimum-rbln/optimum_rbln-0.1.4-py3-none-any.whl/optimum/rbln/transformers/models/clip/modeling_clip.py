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
from typing import TYPE_CHECKING, Optional, Union

import torch
from transformers import AutoConfig, AutoModel, CLIPTextConfig, CLIPTextModel, CLIPTextModelWithProjection
from transformers.models.clip.modeling_clip import CLIPTextModelOutput

from ....modeling_base import RBLNModel
from ....modeling_config import RBLNConfig, RBLNRuntimeConfig


logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from transformers import AutoFeatureExtractor, AutoProcessor, AutoTokenizer, CLIPTextModel


class _TextEncoder(torch.nn.Module):
    def __init__(self, enc: "CLIPTextModel"):
        super().__init__()
        enc.config.return_dict = False
        enc.config.output_hidden_states = True
        self.enc = enc

    def forward(self, inp):
        enc_out = self.enc(inp)
        return enc_out


class RBLNCLIPTextModel(RBLNModel):
    model_type = "rbln_clip"
    auto_model_class = AutoModel  # feature extraction
    original_model_class = CLIPTextModel
    original_config_class = CLIPTextConfig

    def __post_init__(self, **kwargs):
        self.dtype = torch.float32

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        configtmp = AutoConfig.from_pretrained
        modeltmp = AutoModel.from_pretrained
        AutoConfig.from_pretrained = cls.original_config_class.from_pretrained
        AutoModel.from_pretrained = cls.original_model_class.from_pretrained
        rt = super().from_pretrained(*args, **kwargs)
        AutoConfig.from_pretrained = configtmp
        AutoModel.from_pretrained = modeltmp
        return rt

    @classmethod
    def wrap_model_if_needed(cls, model: torch.nn.Module) -> torch.nn.Module:
        return _TextEncoder(model).eval()

    @classmethod
    def _get_rbln_config(
        cls,
        preprocessors: Union["AutoFeatureExtractor", "AutoProcessor", "AutoTokenizer"],
        model_config: "CLIPTextConfig",
        rbln_batch_size: Optional[int] = None,
        rbln_img_width: Optional[int] = None,
        rbln_img_height: Optional[int] = None,
    ) -> RBLNConfig:
        model_config.return_dict = False
        if rbln_batch_size is None:
            rbln_batch_size = 1

        rbln_runtime_config = RBLNRuntimeConfig(
            input_info=[
                (
                    "input_ids",
                    [
                        rbln_batch_size,
                        model_config.max_position_embeddings,
                    ],
                    "int64",
                ),
            ],
        )

        rbln_config = RBLNConfig.from_rbln_runtime_configs([rbln_runtime_config])
        return rbln_config

    def forward(self, input_ids: "torch.Tensor", **kwargs):
        text_output = super().forward(input_ids)
        return CLIPTextModelOutput(
            text_embeds=text_output[0],
            last_hidden_state=text_output[1],
            hidden_states=text_output[2:],
        )


class RBLNCLIPTextModelWithProjection(RBLNCLIPTextModel):
    original_model_class = CLIPTextModelWithProjection
