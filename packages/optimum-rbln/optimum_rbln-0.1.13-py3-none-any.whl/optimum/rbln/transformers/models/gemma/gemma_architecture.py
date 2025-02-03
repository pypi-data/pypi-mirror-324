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

from typing import Dict, List, Optional, Tuple, Union

import torch
from transformers.modeling_outputs import (
    BaseModelOutputWithPast,
)

from ...models.decoderonly import (
    DecoderOnlyDecoderLayer,
    DecoderOnlyWrapper,
    slice_and_unsqueeze_cos_sin,
)
from ...models.decoderonly.decoderonly_architecture import DECODERONLY_ATTENTION_CLASSES


class GemmaWrapper(DecoderOnlyWrapper):
    def get_forward_dict(self):
        forward_dict = {}
        forward_dict.update(
            {
                "wrapper": GemmaModel.forward,
                "model": DecoderOnlyDecoderLayer.forward,
                "decoder_layer": DECODERONLY_ATTENTION_CLASSES[self.attn_implementation].forward,
            }
        )
        return forward_dict


class GemmaModel:
    def forward(
        self,
        input_ids: torch.LongTensor = None,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_values: Optional[List[torch.FloatTensor]] = None,
        batch_ids: Optional[torch.LongTensor] = None,
        inputs_embeds: Optional[torch.FloatTensor] = None,
        use_cache: Optional[bool] = True,
        output_attentions: Optional[bool] = False,
        output_hidden_states: Optional[bool] = False,
        cache_pos_for_partitions: Optional[torch.Tensor] = None,
        kvcache_partition_size: Optional[torch.Tensor] = None,
        forward_dict: Optional[Dict[str, classmethod]] = None,
        rotary_pos_emb=None,
    ) -> Union[Tuple, BaseModelOutputWithPast]:
        # retrieve input_ids and inputs_embeds
        if (input_ids is None) ^ (inputs_embeds is not None):
            raise ValueError(
                "You cannot specify both input_ids and inputs_embeds at the same time, and must specify either one"
            )

        # embed positions
        inputs_embeds = self.embed_tokens(input_ids)
        hidden_states = inputs_embeds

        ##### GEMMA change from llama#####
        hidden_states = hidden_states * (self.config.hidden_size**0.5)

        attention_mask = (1 - attention_mask) * torch.finfo(torch.float16).min

        # get cos,sin vector
        cos, sin = rotary_pos_emb(inputs_embeds, attention_mask.shape[-1])
        cos, sin = slice_and_unsqueeze_cos_sin(cos, sin, position_ids)

        # decoder layers
        all_hidden_states = () if output_hidden_states else None
        all_self_attns = () if output_attentions else None

        for layer_idx, decoder_layer in enumerate(self.layers):
            if output_hidden_states:
                all_hidden_states += (hidden_states,)
            layer_outputs = forward_dict["model"](
                decoder_layer,
                hidden_states,
                layer_idx,
                attention_mask=attention_mask,
                position_ids=position_ids,
                past_key_value=past_key_values,
                output_attentions=output_attentions,
                use_cache=use_cache,
                batch_ids=batch_ids,
                cos=cos,
                sin=sin,
                cache_pos_for_partitions=cache_pos_for_partitions,
                kvcache_partition_size=kvcache_partition_size,
                forward_dict=forward_dict,
            )

            hidden_states = layer_outputs[0]

            updated_cache = layer_outputs[2 if output_attentions else 1]

            if output_attentions:
                all_self_attns += (layer_outputs[1],)

        hidden_states = self.norm(hidden_states)

        # add hidden states from the last decoder layer
        if output_hidden_states:
            all_hidden_states += (hidden_states,)

        # convert RebelDynamicCache to legacy Tuple[Tuple[torch.Tensor]]
        next_cache = updated_cache.to_legacy_cache()

        return BaseModelOutputWithPast(
            last_hidden_state=hidden_states,
            past_key_values=next_cache,
            hidden_states=all_hidden_states,
            attentions=all_self_attns,
        )
