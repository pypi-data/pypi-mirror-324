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
import torch

from ....utils import logging
from ...models.decoderonly import (
    DecoderOnlyAttention,
    DecoderOnlyDecoderLayer,
    DecoderOnlyModel,
    DecoderOnlyWrapper,
    RotaryEmbedding,
)


logger = logging.get_logger(__name__)


class ExaoneForCausalLMWrapper(DecoderOnlyWrapper):
    """A wrapper class for the Exaone model with a language modeling head."""

    def __init__(self, model, max_seq_len, kvcache_partition_len=None):
        super(DecoderOnlyWrapper, self).__init__()
        self.config = model.config
        self.model = self.convert_attribute_name(model.transformer)
        self.lm_head = model.lm_head
        self.rotary_emb = RotaryEmbedding(config=self.config, max_seq_len_cached=max_seq_len)

        if kvcache_partition_len is not None:
            # WORKAROUND : for passing partition length as a value to the rbln compiler.
            # What is actually used is the shape of this tensor.
            self.kvcache_partition_size = torch.zeros(kvcache_partition_len, dtype=torch.int32)
            self.attn_implementation = "flash_attn_rbln"
            logger.info(f"Using rbln-flash-attention. (partition length : {kvcache_partition_len})")
        else:
            self.kvcache_partition_size = None
            self.attn_implementation = "eager"

    @staticmethod
    def convert_attribute_name(model):
        model.embed_tokens = model.wte
        model.norm = model.ln_f
        model.layers = model.h

        for layer in model.layers:
            layer.input_layernorm = layer.ln_1
            layer.self_attn = layer.attn.attention
            layer.post_attention_layernorm = layer.ln_2
            layer.self_attn.o_proj = layer.self_attn.out_proj

        return model

    def get_forward_dict(self):
        forward_dict = {}
        forward_dict.update(
            {
                "wrapper": DecoderOnlyModel.forward,
                "model": DecoderOnlyDecoderLayer.forward,
                "decoder_layer": DecoderOnlyAttention.forward,
            }
        )
        return forward_dict
