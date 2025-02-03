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

import math
from typing import Any, Dict, List, Optional, Tuple, Union

import torch
import torch.nn.functional as F
from torch import nn
from transformers.cache_utils import Cache, DynamicCache
from transformers.modeling_attn_mask_utils import _prepare_4d_causal_attention_mask
from transformers.modeling_outputs import BaseModelOutputWithPast, CausalLMOutputWithPast
from transformers.models.llama.modeling_llama import (
    LlamaAttention,
    LlamaDecoderLayer,
    LlamaForCausalLM,
    LlamaModel,
    LlamaRotaryEmbedding,
)


"""
- define new class to put batch_position as a forward args
- _LlamaForCausalLM receives batch_ids (default=None)
"""


class LlamaDynamicBatchWrapper(torch.nn.Module):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def forward(self, input_ids, attention_mask, cache_position, batch_position, *past_key_values):
        if input_ids.shape[1] == 1:
            rbln_batch_position = None
        else:
            rbln_batch_position = batch_position

        past_kv_list = []
        for i in range(self.model.config.num_hidden_layers):
            cur_kv_layer = []
            for j in range(2):
                cur_kv_layer.append(past_key_values[2 * i + j])
            past_kv_list.append(cur_kv_layer)
        model_output = self.model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            position_ids=cache_position,
            past_key_values=past_kv_list,
            batch_ids=rbln_batch_position,
        )

        return model_output, batch_position


class _LlamaRotaryEmbedding(nn.Module):
    def __init__(self, dim, max_position_embeddings=2048, base=10000, device=None):
        super(LlamaRotaryEmbedding, self).__init__()

        self.dim = dim
        self.max_position_embeddings = max_position_embeddings
        self.base = base
        inv_freq = 1.0 / (self.base ** (torch.arange(0, self.dim, 2).float().to(device) / self.dim))
        self.register_buffer("inv_freq", inv_freq, persistent=False)

        # Build here to make `torch.jit.trace` work.
        seq_len = max_position_embeddings
        device = self.inv_freq.device
        dtype = torch.get_default_dtype()
        self.max_seq_len_cached = seq_len
        t = torch.arange(self.max_seq_len_cached, device=device, dtype=self.inv_freq.dtype)

        freqs = torch.outer(t, self.inv_freq)
        # Different from paper, but it uses a different permutation in order to obtain the same calculation
        emb = torch.cat((freqs, freqs), dim=-1)
        self.register_buffer("cos_cached", emb.cos().to(dtype), persistent=False)
        self.register_buffer("sin_cached", emb.sin().to(dtype), persistent=False)

    def forward(self, x, seq_len=None):
        # x: [bs, num_attention_heads, seq_len, head_size]
        if seq_len > self.max_seq_len_cached:
            self._set_cos_sin_cache(seq_len=seq_len, device=x.device, dtype=x.dtype)

        return (
            self.cos_cached[:seq_len].to(dtype=x.dtype),
            self.sin_cached[:seq_len].to(dtype=x.dtype),
        )


class _LlamaAttention(LlamaAttention):
    # single batch llama attention
    def forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_value: Optional[Cache] = None,
        batch_index: Optional[int] = None,
        output_attentions: bool = False,
        use_cache: bool = False,
        cos: Optional[torch.Tensor] = None,
        sin: Optional[torch.Tensor] = None,
        layer_id: int = 0,
        **kwargs,
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor], Optional[Tuple[torch.Tensor]]]:
        bsz, q_len, _ = hidden_states.size()
        if self.config.pretraining_tp > 1:
            key_value_slicing = (self.num_key_value_heads * self.head_dim) // self.config.pretraining_tp
            query_slices = self.q_proj.weight.split(
                (self.num_heads * self.head_dim) // self.config.pretraining_tp, dim=0
            )
            key_slices = self.k_proj.weight.split(key_value_slicing, dim=0)
            value_slices = self.v_proj.weight.split(key_value_slicing, dim=0)

            query_states = [F.linear(hidden_states, query_slices[i]) for i in range(self.config.pretraining_tp)]
            query_states = torch.cat(query_states, dim=-1)

            key_states = [F.linear(hidden_states, key_slices[i]) for i in range(self.config.pretraining_tp)]
            key_states = torch.cat(key_states, dim=-1)

            value_states = [F.linear(hidden_states, value_slices[i]) for i in range(self.config.pretraining_tp)]
            value_states = torch.cat(value_states, dim=-1)

        else:
            query_states = self.q_proj(hidden_states)
            key_states = self.k_proj(hidden_states)
            value_states = self.v_proj(hidden_states)

        query_states = query_states.view(bsz, q_len, self.num_heads, self.head_dim).transpose(1, 2)
        key_states = key_states.view(bsz, q_len, self.num_key_value_heads, self.head_dim).transpose(1, 2)
        value_states = value_states.view(bsz, q_len, self.num_key_value_heads, self.head_dim).transpose(1, 2)

        kv_seq_len = key_states.shape[-2]
        if past_key_value is not None:
            if self.layer_idx is None:
                raise ValueError(
                    f"The cache structure has changed since version v4.36. If you are using {self.__class__.__name__} "
                    "for auto-regressive decoding with k/v caching, please make sure to initialize the attention class "
                    "with a layer index."
                )
            kv_seq_len += past_key_value.get_usable_length(kv_seq_len, self.layer_idx)
        if layer_id == 0:
            cos, sin = self.rotary_emb(value_states, seq_len=kv_seq_len)
        query_states, key_states, cos, sin = apply_rotary_pos_emb(
            query_states, key_states, cos, sin, position_ids, layer_id
        )
        if past_key_value is not None:
            cache_kwargs = {"sin": sin, "cos": cos}  # Specific to RoPE models
        if (batch_index is None or batch_index == -1) and bsz > 1:
            all_key_states = []
            all_value_states = []
            all_attn_output = []
            for b in range(bsz):
                batch_query_states = query_states[b].unsqueeze(0)
                batch_attention_mask = attention_mask[b].unsqueeze(0)
                batch_key_states = key_states[b].unsqueeze(0)
                batch_value_states = value_states[b].unsqueeze(0)

                # reshape for removing repeat_kv
                batch_key_states = batch_key_states.unsqueeze(2)
                batch_value_states = batch_value_states.unsqueeze(2)
                batch_attention_mask = batch_attention_mask.unsqueeze(2)
                batch_query_states = batch_query_states.view(
                    1, self.num_key_value_heads, self.num_heads // self.num_key_value_heads, q_len, self.head_dim
                )

                batch_key_states, batch_value_states = past_key_value.update(
                    batch_key_states, batch_value_states, self.layer_idx, b, cache_kwargs
                )

                # batch_key_states = repeat_kv(
                #         batch_key_states,
                #         self.num_key_value_groups
                #         )
                # batch_value_states = repeat_kv(
                #         batch_value_states,
                #         self.num_key_value_groups
                #         )

                # attn_weights = torch.matmul(batch_query_states, batch_key_states.transpose(2, 3)) / math.sqrt(self.head_dim)
                # reshape for removing repeat_kv
                attn_weights = torch.matmul(batch_query_states, batch_key_states.transpose(3, 4)) / math.sqrt(
                    self.head_dim
                )

                attn_weights = attn_weights + batch_attention_mask

                # upcast attention to fp32
                attn_weights = nn.functional.softmax(attn_weights, dim=-1, dtype=torch.float32).to(query_states.dtype)
                attn_weights = nn.functional.dropout(attn_weights, p=self.attention_dropout, training=self.training)
                attn_output = torch.matmul(attn_weights, batch_value_states)

                # reshape for removing repeat_kv
                attn_output = attn_output.view(1, self.num_heads, q_len, self.head_dim)

                attn_output = attn_output.transpose(1, 2).contiguous()
                attn_output = attn_output.reshape(1, q_len, self.hidden_size)
                all_key_states.append(batch_key_states)
                all_value_states.append(batch_value_states)
                all_attn_output.append(attn_output)
            key_states = torch.cat(all_key_states, dim=0)
            value_states = torch.cat(all_value_states, dim=0)
            attn_output = torch.cat(all_attn_output, dim=0)

        else:
            assert bsz == 1, "dynamic batch update only support input batch 1"
            if batch_index is None or batch_index == -1:
                batch_index = 0

            # reshape for removing repeat_kv
            key_states = key_states.unsqueeze(2)
            value_states = value_states.unsqueeze(2)
            attention_mask = attention_mask.unsqueeze(2)
            query_states = query_states.view(
                1, self.num_key_value_heads, self.num_heads // self.num_key_value_heads, q_len, self.head_dim
            )

            key_states, value_states = past_key_value.update(
                key_states, value_states, self.layer_idx, batch_index, cache_kwargs, read_first_step=True
            )

            # key_states = repeat_kv(key_states, self.num_key_value_groups)
            # value_states = repeat_kv(value_states, self.num_key_value_groups)

            attn_weights = torch.matmul(query_states, key_states.transpose(3, 4)) / math.sqrt(self.head_dim)

            attn_weights = attn_weights + attention_mask

            # upcast attention to fp32
            attn_weights = nn.functional.softmax(attn_weights, dim=-1, dtype=torch.float32).to(query_states.dtype)
            attn_weights = nn.functional.dropout(attn_weights, p=self.attention_dropout, training=self.training)
            attn_output = torch.matmul(attn_weights, value_states)

            # reshape for removing repeat_kv
            attn_output = attn_output.view(1, self.num_heads, q_len, self.head_dim)

            attn_output = attn_output.transpose(1, 2).contiguous()
            attn_output = attn_output.reshape(bsz, q_len, self.hidden_size)

        if self.config.pretraining_tp > 1:
            attn_output = attn_output.split(self.hidden_size // self.config.pretraining_tp, dim=2)
            o_proj_slices = self.o_proj.weight.split(self.hidden_size // self.config.pretraining_tp, dim=1)
            attn_output = sum([F.linear(attn_output[i], o_proj_slices[i]) for i in range(self.config.pretraining_tp)])
        else:
            attn_output = self.o_proj(attn_output)

        if not output_attentions:
            attn_weights = None

        return attn_output, attn_weights, key_states, value_states, cos, sin


class _LlamaDecoderLayer(LlamaDecoderLayer):
    def forward(
        self,
        hidden_states: torch.Tensor,
        layer_idx: int,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_value: Optional[Tuple[torch.Tensor]] = None,
        output_attentions: Optional[bool] = False,
        use_cache: Optional[bool] = False,
        batch_ids: Optional[torch.LongTensor] = None,
        cos: Optional[torch.Tensor] = None,
        sin: Optional[torch.Tensor] = None,
        layer_id: int = 0,
        **kwargs,
    ) -> Tuple[torch.FloatTensor, Optional[Tuple[torch.FloatTensor, torch.FloatTensor]]]:
        residual = hidden_states

        hidden_states = self.input_layernorm(hidden_states)
        bsz, _, _ = hidden_states.size()

        hidden_states, self_attn_weights, k, v, cos, sin = _LlamaAttention.forward(
            self.self_attn,
            hidden_states=hidden_states,
            attention_mask=attention_mask,
            position_ids=position_ids,
            past_key_value=past_key_value,
            output_attentions=output_attentions,
            batch_index=batch_ids,
            use_cache=use_cache,
            cos=cos,
            sin=sin,
            layer_id=layer_id,
            **kwargs,
        )
        past_key_value.assign(k, v, layer_idx)

        present_key_value = past_key_value

        hidden_states = residual + hidden_states

        # Fully Connected
        residual = hidden_states
        hidden_states = self.post_attention_layernorm(hidden_states)
        hidden_states = self.mlp(hidden_states)
        hidden_states = residual + hidden_states

        outputs = (hidden_states,)

        if output_attentions:
            outputs += (self_attn_weights,)

        if use_cache:
            outputs += (present_key_value,)

        return outputs, cos, sin


class _LlamaModel(LlamaModel):
    def forward(
        self,
        input_ids: torch.LongTensor = None,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_values: Optional[List[torch.FloatTensor]] = None,
        batch_ids: Optional[torch.LongTensor] = None,
        inputs_embeds: Optional[torch.FloatTensor] = None,
        use_cache: Optional[bool] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
    ) -> Union[Tuple, BaseModelOutputWithPast]:
        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        use_cache = use_cache if use_cache is not None else self.config.use_cache

        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        #### cannot change forward args? temporal workaround ####
        # current_step = position_ids

        # retrieve input_ids and inputs_embeds
        if input_ids is not None and inputs_embeds is not None:
            raise ValueError("You cannot specify both input_ids and inputs_embeds at the same time")
        elif input_ids is not None:
            batch_size, seq_length = input_ids.shape[:2]
        elif inputs_embeds is not None:
            batch_size, seq_length = inputs_embeds.shape[:2]
        else:
            raise ValueError("You have to specify either input_ids or inputs_embeds")

        past_key_values_length = 0
        if use_cache:
            use_legacy_cache = not isinstance(past_key_values, Cache)
            if use_legacy_cache:
                past_key_values = RebelDynamicCache.from_legacy_cache(
                    position_ids=position_ids,
                    max_length=self.config.max_position_embeddings,
                    past_key_values=past_key_values,
                )

            # not used, get_usable_length will be changed
            # past_key_values_length = past_key_values.get_usable_length(seq_length)

        #### position embedding indice ####
        # position_ids = torch.arange(0, input_ids.shape[-1], dtype=torch.int32).unsqueeze(0) + current_step

        if position_ids is None:
            device = input_ids.device if input_ids is not None else inputs_embeds.device
            position_ids = torch.arange(
                past_key_values_length, seq_length + past_key_values_length, dtype=torch.long, device=device
            )
            position_ids = position_ids.unsqueeze(0)

        if inputs_embeds is None:
            inputs_embeds = self.embed_tokens(input_ids)

        # ##### original condition for generating causal attention mask
        # if getattr(self.config, "_flash_attn_2_enabled", False):
        #     # 2d mask is passed through the layers
        #     attention_mask = attention_mask if (attention_mask is not None and 0 in attention_mask) else None

        # else:
        #     # 4d mask is passed through the layers
        #     attention_mask = _prepare_4d_causal_attention_mask(
        #         attention_mask, (batch_size, seq_length), inputs_embeds, past_key_values_length
        #     )
        # ########################################################

        # yhboo changed for valid graph generation
        if getattr(self.config, "_flash_attn_2_enabled", False):
            # 2d mask is passed through the layers
            attention_mask = attention_mask if (attention_mask is not None and 0 in attention_mask) else None
            raise NotImplementedError

        elif attention_mask is not None and attention_mask.ndim == 4:
            # assuming attention mask is generated as input
            # assumed dim = [batch_size, 1, inp_seq, max_seq]
            # only make [1, 0] mask to [0, -inf]
            attention_mask = (1 - attention_mask) * torch.finfo(torch.float16).min

        else:
            # 4d mask is passed through the layers
            attention_mask = _prepare_4d_causal_attention_mask(
                attention_mask, (batch_size, seq_length), inputs_embeds, past_key_values_length
            )

        # embed positions
        hidden_states = inputs_embeds

        # decoder layers
        all_hidden_states = () if output_hidden_states else None
        all_self_attns = () if output_attentions else None
        next_decoder_cache = () if use_cache else None

        cos = None
        sin = None
        for layer_idx, decoder_layer in enumerate(self.layers):
            if output_hidden_states:
                all_hidden_states += (hidden_states,)
            layer_outputs = _LlamaDecoderLayer.forward(
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
                layer_id=layer_idx,
            )
            cos = layer_outputs[-2]
            sin = layer_outputs[-1]
            layer_outputs = layer_outputs[0]

            hidden_states = layer_outputs[0]

            if use_cache:
                next_decoder_cache = layer_outputs[2 if output_attentions else 1]

            if output_attentions:
                all_self_attns += (layer_outputs[1],)

        hidden_states = self.norm(hidden_states)

        # add hidden states from the last decoder layer
        if output_hidden_states:
            all_hidden_states += (hidden_states,)

        next_cache = None
        if use_cache:
            next_cache = next_decoder_cache.to_legacy_cache() if use_legacy_cache else next_decoder_cache

        return BaseModelOutputWithPast(
            last_hidden_state=hidden_states,
            past_key_values=next_cache,
            hidden_states=all_hidden_states,
            attentions=all_self_attns,
        )


class _LlamaForCausalLM(LlamaForCausalLM):
    def forward(
        self,
        input_ids: torch.LongTensor = None,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_values: Optional[List[torch.FloatTensor]] = None,
        batch_ids: Optional[torch.LongTensor] = None,
        inputs_embeds: Optional[torch.FloatTensor] = None,
        labels: Optional[torch.LongTensor] = None,
        use_cache: Optional[bool] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
    ) -> Union[Tuple, CausalLMOutputWithPast]:
        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        # decoder outputs consists of (dec_features, layer_state, dec_hidden, dec_attn)
        outputs = self.model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            position_ids=position_ids,
            past_key_values=past_key_values,
            inputs_embeds=inputs_embeds,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
            batch_ids=batch_ids,
        )

        hidden_states = outputs[0]
        logits = self.lm_head(hidden_states)
        logits = logits.float()

        if not return_dict:
            output = (logits,) + outputs[1:]
            return output

        return CausalLMOutputWithPast(
            logits=logits,
            past_key_values=outputs.past_key_values,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions,
        )


class RebelDynamicCache(DynamicCache):
    """
    A cache that grows dynamically as more tokens are generated. This is the default for generative models.

    It stores the Key and Value states as a list of tensors, one for each layer. The expected shape for each tensor is
    `[batch_size, num_heads, seq_len, head_dim]`.
    """

    def __init__(self, current_steps, max_length) -> None:
        super().__init__()
        self.current_steps = current_steps
        self.max_length = max_length

    def assign(
        self,
        key_states: torch.Tensor,
        value_states: torch.Tensor,
        layer_idx: int,
    ) -> None:
        self.key_cache[layer_idx] = key_states.squeeze(2)
        self.value_cache[layer_idx] = value_states.squeeze(2)

    def batch_select_assign(
        self,
        key_states: torch.Tensor,
        value_states: torch.Tensor,
        batch_ids: int,
        layer_idx: int,
    ) -> None:
        past_key = self.key_cache[layer_idx]
        past_value = self.value_cache[layer_idx]

        ## (ISSUE): relay scatter_element index have same shape as cache.. can remove?
        # update_key = past_key.slice_scatter(key_states, dim = 0, start=batch_ids, end=batch_ids+1)
        # update_value = past_value.slice_scatter(value_states, dim = 0, start=batch_ids, end=batch_ids+1)

        ## (ISSUE): torch select_scatter fits to the purpose (always replace single index), but not implmeneted to TVM yet..
        # update_key = past_key.select_scatter(key_states.squeeze(0), dim = 0, index=batch_ids)
        # update_value = past_value.select_scatter(value_states.squeeze(0), dim = 0, index=batch_ids)
        cache_batch_size = past_key.shape[0]
        if cache_batch_size == 1:
            self.key_cache[layer_idx] = key_states
            self.value_cache[layer_idx] = value_states
        else:
            update_key = [key_states]
            update_value = [value_states]
            for i in range(1, cache_batch_size):
                update_key.append(past_key[i : i + 1])
                update_value.append(past_value[i : i + 1])
            update_key = torch.cat(update_key, dim=0)
            update_value = torch.cat(update_value, dim=0)
            self.key_cache[layer_idx] = update_key
            self.value_cache[layer_idx] = update_value

        ## (ISSUE): tvm copy issue
        # past_key[batch_ids] = key_states
        # past_value[batch_ids] = value_states
        # self.key_cache[layer_idx] = past_key
        # self.value_cache[layer_idx] = past_value

    def copy(
        self,
        key_states: torch.Tensor,
        value_states: torch.Tensor,
        layer_idx: int,
        cache_kwargs: Optional[Dict[str, Any]] = None,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Copy the cache with the new `key_states` and `value_states` for the layer `layer_idx`.
        just for from_legacy_cache function

        Parameters:
            key_states (`torch.Tensor`):
                The new key states to cache.
            value_states (`torch.Tensor`):
                The new value states to cache.
            layer_idx (`int`):
                The index of the layer to cache the states for.
            cache_kwargs (`Dict[str, Any]`, `optional`):
                Additional arguments for the cache subclass. No additional arguments are used in `DynamicCache`.

        Return:
            A tuple containing the updated key and value states.
        """
        # Update the number of seen tokens : deprecated
        # if layer_idx == 0:
        #     self.seen_tokens += key_states.shape[-2]

        # Update the cache
        if len(self.key_cache) <= layer_idx:
            self.key_cache.append(key_states)
            self.value_cache.append(value_states)
        else:
            self.key_cache[layer_idx] = torch.cat([self.key_cache[layer_idx], key_states], dim=-2)
            self.value_cache[layer_idx] = torch.cat([self.value_cache[layer_idx], value_states], dim=-2)

        return self.key_cache[layer_idx], self.value_cache[layer_idx]

    def update(
        self,
        key_states: torch.Tensor,
        value_states: torch.Tensor,
        layer_idx: int,
        batch_index: int,
        cache_kwargs: Optional[Dict[str, Any]] = None,
        read_first_step: Optional[bool] = False,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Updates the cache with the new `key_states` and `value_states` for the layer `layer_idx`
        based on self.current_step,

        Parameters:
            key_states (`torch.Tensor`):
                The new key states to cache.
            value_states (`torch.Tensor`):
                The new value states to cache.
            layer_idx (`int`):
                The index of the layer to cache the states for.
            cache_kwargs (`Dict[str, Any]`, `optional`):
                Additional arguments for the cache subclass. No additional arguments are used in `DynamicCache`.

        Return:
            A tuple containing the updated key and value states.
        """
        # # Update the number of seen tokens : deprecated
        # if layer_idx == 0:
        #     self.seen_tokens += key_states.shape[-2]

        # Update the cache
        if len(self.key_cache) <= layer_idx:
            self.key_cache.append(key_states)
            self.value_cache.append(value_states)
        else:
            # [B,H,M,D]
            # kv cache = [B, H, 4096, D]
            # states = [1, H, 128, D]
            # want to update states into kv_cache[batch_index][current_step]
            # import pdb; pdb.set_trace()
            current_step = self.current_steps[0 if read_first_step else batch_index]
            kend = current_step + key_states.shape[-2]
            vend = current_step + value_states.shape[-2]
            update_key_states = (
                self.key_cache[layer_idx][batch_index]
                .unsqueeze(0)
                .unsqueeze(2)
                .slice_scatter(key_states, dim=-2, start=current_step, end=kend)
            )
            update_value_states = (
                self.value_cache[layer_idx][batch_index]
                .unsqueeze(0)
                .unsqueeze(2)
                .slice_scatter(value_states, dim=-2, start=current_step, end=vend)
            )
        return update_key_states, update_value_states

    def get_seq_length(self, layer_idx: Optional[int] = 0) -> int:
        """Returns the sequence length of the cached states. A layer index can be optionally passed."""
        if len(self.key_cache) <= layer_idx:
            return 0
        return self.key_cache[layer_idx].shape[-2]

    def get_max_length(self) -> Optional[int]:
        return self.max_length

    @classmethod
    def from_legacy_cache(
        cls, position_ids, max_length, past_key_values: Optional[Tuple[Tuple[torch.FloatTensor]]] = None
    ) -> "DynamicCache":
        """Converts a cache in the legacy cache format into an equivalent `DynamicCache`."""
        batch, seq_len = position_ids.shape
        # make current_steps lists from position_ids
        # position_ids[b][0] is equal to cache position of each batch
        current_steps = [position_ids[b][0] for b in range(batch)]
        assert len(current_steps) == batch
        cache = cls(current_steps, max_length)
        if past_key_values is not None:
            for layer_idx in range(len(past_key_values)):
                key_states, value_states = past_key_values[layer_idx]
                cache.copy(key_states, value_states, layer_idx)
        return cache


def rotate_half(x):
    """Rotates half the hidden dims of the input."""
    x1 = x[..., : x.shape[-1] // 2]
    x2 = x[..., x.shape[-1] // 2 :]
    return torch.cat((-x2, x1), dim=-1)


def apply_rotary_pos_emb(q, k, cos, sin, position_ids, layer_id, unsqueeze_dim=1):
    """Applies Rotary Position Embedding to the query and key tensors.

    Args:
        q (`torch.Tensor`): The query tensor.
        k (`torch.Tensor`): The key tensor.
        cos (`torch.Tensor`): The cosine part of the rotary embedding.
        sin (`torch.Tensor`): The sine part of the rotary embedding.
        position_ids (`torch.Tensor`):
            The position indices of the tokens corresponding to the query and key tensors. For example, this can be
            used to pass offsetted position ids when working with a KV-cache.
        unsqueeze_dim (`int`, *optional*, defaults to 1):
            The 'unsqueeze_dim' argument specifies the dimension along which to unsqueeze cos[position_ids] and
            sin[position_ids] so that they can be properly broadcasted to the dimensions of q and k. For example, note
            that cos[position_ids] and sin[position_ids] have the shape [batch_size, seq_len, head_dim]. Then, if q and
            k have the shape [batch_size, heads, seq_len, head_dim], then setting unsqueeze_dim=1 makes
            cos[position_ids] and sin[position_ids] broadcastable to the shapes of q and k. Similarly, if q and k have
            the shape [batch_size, seq_len, heads, head_dim], then set unsqueeze_dim=2.
    Returns:
        `tuple(torch.Tensor)` comprising of the query and key tensors rotated using the Rotary Position Embedding.
    """
    if layer_id == 0:
        if position_ids.shape[0] > 1:
            cos_all = []
            sin_all = []
            for i in range(position_ids.shape[0]):
                cos_all.append(cos[position_ids[i : i + 1]].unsqueeze(unsqueeze_dim))
                sin_all.append(sin[position_ids[i : i + 1]].unsqueeze(unsqueeze_dim))
            cos = torch.cat(cos_all, dim=0)
            sin = torch.cat(sin_all, dim=0)
        else:
            cos = cos[position_ids].unsqueeze(unsqueeze_dim)
            sin = sin[position_ids].unsqueeze(unsqueeze_dim)
        # cos = cos[position_ids].unsqueeze(unsqueeze_dim)
        # sin = sin[position_ids].unsqueeze(unsqueeze_dim)

    q_embed = (q * cos) + (rotate_half(q) * sin)
    k_embed = (k * cos) + (rotate_half(k) * sin)
    return q_embed, k_embed, cos, sin


def wrap_llama():
    LlamaRotaryEmbedding.__init__ = _LlamaRotaryEmbedding.__init__
    LlamaRotaryEmbedding.forward = _LlamaRotaryEmbedding.forward
    LlamaModel.forward = _LlamaModel.forward
    LlamaForCausalLM.forward = _LlamaForCausalLM.forward
