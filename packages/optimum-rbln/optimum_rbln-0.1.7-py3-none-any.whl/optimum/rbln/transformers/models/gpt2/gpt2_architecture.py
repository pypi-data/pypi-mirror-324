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

from typing import List, Optional, Tuple, Union

import torch
import torch.nn as nn
from transformers.modeling_outputs import (
    BaseModelOutputWithPast,
    BaseModelOutputWithPastAndCrossAttentions,
)
from transformers.models.gpt2.modeling_gpt2 import GPT2Attention, GPT2Block, GPT2Model


class _GPT2Attention(GPT2Attention):
    def _attn(self, query, key, value, attention_mask=None, head_mask=None):
        attn_weights = torch.matmul(query, key.transpose(-1, -2))

        if self.scale_attn_weights:
            attn_weights = attn_weights / torch.full(
                [], value.size(-1) ** 0.5, dtype=attn_weights.dtype, device=attn_weights.device
            )

        # Layer-wise attention scaling
        if self.scale_attn_by_inverse_layer_idx:
            attn_weights = attn_weights / float(self.layer_idx + 1)

        # -------------------
        # Below are deleted since "where" op does not supported on RBLN graph.
        # -------------------
        # if not self.is_cross_attention:
        #     # if only "normal" attention layer implements causal mask
        #     query_length, key_length = query.size(-2), key.size(-2)
        #     causal_mask = self.bias[:, :, key_length - query_length : key_length, :key_length]
        #     mask_value = torch.finfo(attn_weights.dtype).min
        #     # Need to be a tensor, otherwise we get error: `RuntimeError: expected scalar type float but found double`.
        #     # Need to be on the same device, otherwise `RuntimeError: ..., x and y to be on the same device`
        #     mask_value = torch.full([], mask_value, dtype=attn_weights.dtype, device=attn_weights.device)
        #     attn_weights = torch.where(causal_mask, attn_weights.to(attn_weights.dtype), mask_value)

        if attention_mask is not None:
            # Apply the attention mask
            attn_weights = attn_weights + attention_mask

        attn_weights = nn.functional.softmax(attn_weights, dim=-1)

        # Downcast (if necessary) back to V's dtype (if in mixed-precision) -- No-Op otherwise
        attn_weights = attn_weights.type(value.dtype)
        # attn_weights = self.attn_dropout(attn_weights)

        # Mask heads if we want to
        if head_mask is not None:
            attn_weights = attn_weights * head_mask

        attn_output = torch.matmul(attn_weights, value)

        return attn_output, attn_weights

    def forward(
        self,
        hidden_states: Optional[Tuple[torch.FloatTensor]],
        past_key_values: List[List[torch.Tensor]] = None,
        attention_mask: Optional[torch.FloatTensor] = None,
        head_mask: Optional[torch.FloatTensor] = None,
        encoder_hidden_states: Optional[torch.Tensor] = None,
        encoder_attention_mask: Optional[torch.FloatTensor] = None,
        use_cache: Optional[bool] = False,
        output_attentions: Optional[bool] = False,
        cache_position: Optional[torch.LongTensor] = None,
    ) -> Tuple[Union[torch.Tensor, Tuple[torch.Tensor]], ...]:
        query, key, value = self.c_attn(hidden_states).split(self.split_size, dim=2)

        query = self._split_heads(query, self.num_heads, self.head_dim)
        key = self._split_heads(key, self.num_heads, self.head_dim)
        value = self._split_heads(value, self.num_heads, self.head_dim)

        if past_key_values is not None:
            past_key, past_value = past_key_values[self.layer_idx]
            query_length = query.shape[-2]

            key = past_key.slice_scatter(key, dim=2, start=cache_position, end=cache_position + query_length)
            value = past_value.slice_scatter(value, dim=2, start=cache_position, end=cache_position + query_length)

            past_key_values[self.layer_idx] = [key, value]

        attn_output, _ = _GPT2Attention._attn(self, query, key, value, attention_mask, head_mask)

        attn_output = self._merge_heads(attn_output, self.num_heads, self.head_dim)

        attn_output = self.c_proj(attn_output)
        attn_output = self.resid_dropout(attn_output)

        return attn_output


class _GPT2Block(GPT2Block):
    def forward(
        self,
        hidden_states: Optional[Tuple[torch.FloatTensor]],
        past_key_values: List[List[torch.Tensor]] = None,
        attention_mask: Optional[torch.FloatTensor] = None,
        head_mask: Optional[torch.FloatTensor] = None,
        encoder_hidden_states: Optional[torch.Tensor] = None,
        encoder_attention_mask: Optional[torch.FloatTensor] = None,
        use_cache: Optional[bool] = False,
        output_attentions: Optional[bool] = False,
        cache_position: Optional[torch.LongTensor] = None,
    ) -> Union[Tuple[torch.Tensor], Optional[Tuple[torch.Tensor, Tuple[torch.FloatTensor, ...]]]]:
        residual = hidden_states
        hidden_states = self.ln_1(hidden_states)

        attn_output = _GPT2Attention.forward(
            self.attn,
            hidden_states,
            past_key_values=past_key_values,
            attention_mask=attention_mask,
            head_mask=head_mask,
            cache_position=cache_position,
        )

        # residual connection
        hidden_states = attn_output + residual

        residual = hidden_states
        hidden_states = self.ln_2(hidden_states)
        feed_forward_hidden_states = self.mlp(hidden_states)
        # residual connection
        hidden_states = residual + feed_forward_hidden_states

        return hidden_states


class _GPT2Model(GPT2Model):
    def forward(
        self,
        input_ids: Optional[torch.LongTensor] = None,
        past_key_values: List[List[torch.Tensor]] = None,
        attention_mask: Optional[torch.FloatTensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        head_mask: Optional[torch.FloatTensor] = None,
        cache_position: Optional[torch.LongTensor] = None,
    ) -> Union[Tuple, BaseModelOutputWithPastAndCrossAttentions]:
        input_shape = input_ids.size()

        if position_ids is None:
            # force dtype to torch.long -> torch.int32 (to match cache_position)
            position_ids = torch.arange(0, input_shape[-1], dtype=torch.int32) + cache_position
            position_ids = position_ids.unsqueeze(0)

        # GPT2Attention mask.
        # Here we assume mask is causal mask, (batch, 1, query_length, key_length + query_length)
        attention_mask = (1.0 - attention_mask) * torch.finfo(self.dtype).min

        # Prepare head mask if needed
        # 1.0 in head_mask indicate we keep the head
        # attention_probs has shape bsz x n_heads x N x N
        # head_mask has shape n_layer x batch x n_heads x N x N
        head_mask = self.get_head_mask(head_mask, self.config.n_layer)

        inputs_embeds = self.wte(input_ids)
        position_embeds = self.wpe(position_ids)
        hidden_states = inputs_embeds + position_embeds

        hidden_states = self.drop(hidden_states)

        output_shape = (-1,) + input_shape[1:] + (hidden_states.size(-1),)

        for i, block in enumerate(self.h):
            hidden_states = _GPT2Block.forward(
                block,
                hidden_states,
                past_key_values=past_key_values,
                attention_mask=attention_mask,
                head_mask=head_mask[i],
                cache_position=cache_position,
            )

        hidden_states = self.ln_f(hidden_states)
        hidden_states = hidden_states.view(output_shape)
        return BaseModelOutputWithPast(last_hidden_state=hidden_states, past_key_values=past_key_values)


class GPT2LMHeadModelWrapper(torch.nn.Module):
    def __init__(self, gpt):
        super().__init__()
        self.model = gpt

    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor,
        cache_position: torch.LongTensor,
        *past_key_values: torch.Tensor,
    ):
        kv_cache = []
        for i in range(self.model.config.n_layer):
            kv_cache.append((past_key_values[2 * i], past_key_values[2 * i + 1]))

        transformer_outputs = _GPT2Model.forward(
            self.model.transformer,
            input_ids=input_ids,
            past_key_values=kv_cache,
            attention_mask=attention_mask,
            cache_position=cache_position,
        )

        hidden_states = transformer_outputs[0]

        # TODO : Use query_length here to pick last logit
        # batch_size, sequence_length = hidden_states.shape[:2]
        # hidden_states = hidden_states.view(batch_size * sequence_length, -1)
        # hidden_states = torch.nn.functional.embedding(query_length, hidden_states)
        # hidden_states = hidden_states.view(batch_size, 1, -1)

        lm_logits = self.model.lm_head(hidden_states)
        kv_cache = transformer_outputs[1]

        past_key_values = []
        for i in range(self.model.config.n_layer):
            past_key_values.append(kv_cache[i][0])
            past_key_values.append(kv_cache[i][1])

        output = (lm_logits,) + tuple(past_key_values)
        return output
