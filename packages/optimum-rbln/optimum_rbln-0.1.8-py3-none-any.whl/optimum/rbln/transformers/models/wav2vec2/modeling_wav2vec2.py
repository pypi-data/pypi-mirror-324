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
from transformers import AutoModelForMaskedLM, PretrainedConfig, Wav2Vec2ForCTC
from transformers.modeling_outputs import CausalLMOutput

from ....modeling_base import RBLNModel
from ....modeling_config import RBLNConfig, RBLNRuntimeConfig


logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from transformers import (
        AutoFeatureExtractor,
        AutoProcessor,
        AutoTokenizer,
        PretrainedConfig,
    )


class _Wav2Vec2(torch.nn.Module):
    def __init__(self, model: "Wav2Vec2ForCTC"):
        super().__init__()
        self.model = model

    def forward(self, input_values):
        output = self.model.wav2vec2(input_values=input_values)
        return self.model.lm_head(output[0])


class RBLNWav2Vec2ForCTC(RBLNModel):
    """
    Wav2Vec2 Model with a `language modeling` head on top for Connectionist Temporal Classification (CTC).

    This model inherits from [`RBLNModel`]. Check the superclass documentation for the generic methods the
    library implements for all its model.

    It implements the methods to convert a pre-trained Wav2Vec2 model into a RBLN Wav2Vec2 model by:
    - transferring the checkpoint weights of the original into an optimized RBLN graph,
    - compiling the resulting graph using the RBLN compiler.
    """

    model_type = "rbln_model"
    main_input_name = "input_values"
    auto_model_class = AutoModelForMaskedLM

    @classmethod
    def wrap_model_if_needed(cls, model: torch.nn.Module) -> torch.nn.Module:
        return _Wav2Vec2(model).eval()

    @classmethod
    def _get_rbln_config(
        cls,
        preprocessors: Union["AutoFeatureExtractor", "AutoProcessor", "AutoTokenizer"],
        model_config: "PretrainedConfig",
        rbln_max_seq_len: Optional[int] = None,
        rbln_batch_size: Optional[int] = None,
    ) -> RBLNConfig:
        meta = {}

        if rbln_max_seq_len is None:
            for tokenizer in preprocessors:
                if hasattr(tokenizer, "model_max_length"):
                    rbln_max_seq_len = tokenizer.model_max_length
                    break
            if rbln_max_seq_len is None:
                raise ValueError("`rbln_max_seq_len` should be specified!")

        meta["rbln_max_seq_len"] = rbln_max_seq_len

        if rbln_batch_size is None:
            rbln_batch_size = 1

        input_info = [
            (
                "input_values",
                [
                    rbln_batch_size,
                    rbln_max_seq_len,
                ],
                "float32",
            ),
        ]

        rbln_runtime_config = RBLNRuntimeConfig(input_info=input_info, batch_size=rbln_batch_size)

        rbln_config = RBLNConfig.from_rbln_runtime_configs(
            [rbln_runtime_config],
            _rbln_meta=meta,
        )

        return rbln_config

    def forward(self, input_values: "torch.Tensor", **kwargs):
        outputs = super().forward(input_values, **kwargs)
        return CausalLMOutput(logits=outputs)
