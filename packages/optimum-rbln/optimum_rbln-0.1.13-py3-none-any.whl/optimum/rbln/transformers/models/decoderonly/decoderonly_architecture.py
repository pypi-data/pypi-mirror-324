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
from typing import Dict, Optional, Tuple

import torch
from torch import nn
from transformers import PretrainedConfig
from transformers.modeling_outputs import (
    BaseModelOutputWithPast,
)

from ....utils import logging
from ...cache_utils import RebelDynamicCache
from ...modeling_rope_utils import ROPE_INIT_FUNCTIONS


logger = logging.get_logger(__name__)
"""
##############################################################################
# RBLN custom operation (python interface)
# torch.compile custom operation
# torch.library.define - kernel declaration
# torch.library.impl - kernel implementation
# torch.library.impl_abstract - symbolic trace
##############################################################################
"""

# RBLN custom op(flash attention decode)
torch.library.define(
    "rbln_custom_ops::flash_attn_decode",
    "(Tensor x, Tensor y, Tensor z, Tensor w, Tensor a, Tensor b, Tensor c, Tensor d) -> Tensor[]",
)


@torch.library.impl("rbln_custom_ops::flash_attn_decode", "cpu")
def flash_attn_decode_cpu(q, k, v, mask, kcache, vcache, seq, partition):
    """
    WORKAROUND:
    Partition is declared as an argument to the function, even though it is
    not actually used in the CPU implementation, this allows the rbln compiler
    to perform flash attention operations with partition as an argument.
    """
    assert kcache.dim() == k.dim()
    assert vcache.dim() == v.dim()
    assert k.size(-2) == v.size(-2)
    assert partition.dim() == 1
    b = 0
    if seq.dim() == 1:
        s = seq[0]
    elif seq.dim() == 0:
        s = seq
    else:
        assert False
    e = s + k.size(-2)
    updated_k = kcache[b].unsqueeze(0).slice_scatter(k, dim=-2, start=s, end=e)
    updated_v = vcache[b].unsqueeze(0).slice_scatter(v, dim=-2, start=s, end=e)
    attn_weight = torch.matmul(q, updated_k.transpose(3, 4)) / math.sqrt(128)
    attn_weight = attn_weight + mask
    attn_weight = nn.functional.softmax(attn_weight, dim=-1, dtype=torch.float32).to(q.dtype)
    attn_output = torch.matmul(attn_weight, updated_v)
    return attn_output, torch.empty_like(kcache), torch.empty_like(vcache)


@torch.library.impl_abstract("rbln_custom_ops::flash_attn_decode")
def flash_attn_decode_abstract(q, k, v, m, kcache, vcache, seq, partition):
    return torch.empty_like(q), torch.empty_like(kcache), torch.empty_like(vcache)


# RBLN custom op(flash attention prefill)
torch.library.define(
    "rbln_custom_ops::flash_attn_prefill",
    "(Tensor x, Tensor y, Tensor z, Tensor w, Tensor a, Tensor b, Tensor c, Tensor d, Tensor e) -> Tensor[]",
)


@torch.library.impl("rbln_custom_ops::flash_attn_prefill", "cpu")
def flash_attn_prefill_cpu(q, k, v, mask, kcache, vcache, batch, seq, partition):
    """
    WORKAROUND:
    Partition is declared as an argument to the function, even though it is
    not actually used in the CPU implementation, this allows the rbln compiler
    to perform flash attention operations with partition as an argument.
    """
    assert kcache.dim() == k.dim()
    assert vcache.dim() == v.dim()
    assert k.size(-2) == v.size(-2)
    assert partition.dim() == 1
    if batch.dim() == 1:
        b = batch[0]
    elif batch.dim() == 0:
        b = batch
    else:
        assert False
    if seq.dim() == 1:
        s = seq[0]
    elif seq.dim() == 0:
        s = seq
    else:
        assert False
    e = s + k.size(-2)
    updated_k = kcache[b].unsqueeze(0).slice_scatter(k, dim=-2, start=s, end=e)
    updated_v = vcache[b].unsqueeze(0).slice_scatter(v, dim=-2, start=s, end=e)
    attn_weight = torch.matmul(q, updated_k.transpose(3, 4)) / math.sqrt(128)
    attn_weight = attn_weight + mask
    attn_weight = nn.functional.softmax(attn_weight, dim=-1, dtype=torch.float32).to(q.dtype)
    attn_output = torch.matmul(attn_weight, updated_v)
    return attn_output, torch.empty_like(kcache), torch.empty_like(vcache)


@torch.library.impl_abstract("rbln_custom_ops::flash_attn_prefill")
def flash_attn_prefill_abstract(q, k, v, m, kcache, vcache, batch, seq, partition):
    return torch.empty_like(q), torch.empty_like(kcache), torch.empty_like(vcache)


# RBLN custom op(cache update)
torch.library.define("rbln_custom_ops::rbln_cache_update", "(Tensor x, Tensor y, Tensor z, Tensor w) -> Tensor")


@torch.library.impl("rbln_custom_ops::rbln_cache_update", "cpu")
def rbln_cache_update_cpu(cache, value, batch, seq):
    updated_cache = cache[batch].slice_scatter(value, dim=-2, start=batch[0], end=batch[0] + seq[0])
    return updated_cache


@torch.library.impl_abstract("rbln_custom_ops::rbln_cache_update")
def rbln_cache_update_abstract(cache, value, batch, seq):
    return torch.empty_like(cache)


class DecoderOnlyAttention:
    def _attn(self, query_state, key_state, value_state, attn_mask, past_key_value, batch_idx=0, is_prefill=False):
        # reshape for removing repeat_kv (batch=1 , num_head, 1, q_len=1, head_dim)
        key_state = key_state.unsqueeze(2)
        value_state = value_state.unsqueeze(2)
        attn_mask = attn_mask.unsqueeze(2)

        query_state = query_state.view(
            1,
            self.num_key_value_heads,
            self.num_heads // self.num_key_value_heads,
            -1,
            self.head_dim,
        )

        key_state, value_state = past_key_value.update(
            key_state, value_state, self.layer_idx, batch_idx, read_first_step=is_prefill
        )

        attn_weight = torch.matmul(query_state, key_state.transpose(3, 4)) / math.sqrt(self.head_dim)
        attn_weight += attn_mask
        attn_weight = nn.functional.softmax(attn_weight, dim=-1, dtype=torch.float32).to(query_state.dtype)
        attn_output = torch.matmul(attn_weight, value_state)

        attn_output = attn_output.view(1, self.num_heads, -1, self.head_dim)
        attn_output = attn_output.transpose(1, 2).contiguous()
        attn_output = attn_output.reshape(1, -1, self.num_heads * self.head_dim)

        return attn_output, key_state, value_state

    def forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_value: Optional[RebelDynamicCache] = None,
        batch_index: Optional[torch.Tensor] = None,
        output_attentions: bool = False,
        cos: Optional[torch.Tensor] = None,
        sin: Optional[torch.Tensor] = None,
        **kwargs,
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor], Optional[Tuple[torch.Tensor]]]:
        bsz, q_len, _ = hidden_states.size()
        query_states = self.q_proj(hidden_states)
        key_states = self.k_proj(hidden_states)
        value_states = self.v_proj(hidden_states)

        query_states = query_states.view(bsz, q_len, self.num_heads, self.head_dim).transpose(1, 2)
        key_states = key_states.view(bsz, q_len, self.num_key_value_heads, self.head_dim).transpose(1, 2)
        value_states = value_states.view(bsz, q_len, self.num_key_value_heads, self.head_dim).transpose(1, 2)

        query_states, key_states = apply_rotary_pos_emb(query_states, key_states, cos, sin)

        # Decoder (bsz > 1)
        if bsz > 1:
            iterate_results = {"key_states": [], "value_states": [], "attn_output": []}
            for b in range(bsz):
                attn_output, key_state, value_state = DecoderOnlyAttention._attn(
                    self,
                    query_states[b].unsqueeze(0),
                    key_states[b].unsqueeze(0),
                    value_states[b].unsqueeze(0),
                    attention_mask[b].unsqueeze(0),
                    past_key_value,
                    batch_idx=b,
                    is_prefill=False,
                )

                iterate_results["key_states"].append(key_state)
                iterate_results["value_states"].append(value_state)
                iterate_results["attn_output"].append(attn_output)

            key_states = torch.cat(iterate_results["key_states"], dim=0)
            value_states = torch.cat(iterate_results["value_states"], dim=0)
            attn_output = torch.cat(iterate_results["attn_output"], dim=0)
        # Prefill & Decoder (bsz == 1)
        else:
            attn_output, key_states, value_states = DecoderOnlyAttention._attn(
                self,
                query_states,
                key_states,
                value_states,
                attention_mask,
                past_key_value,
                batch_idx=batch_index,
                is_prefill=True,
            )

        attn_output = self.o_proj(attn_output)

        if not output_attentions:
            attn_weight = None

        return attn_output, attn_weight, key_states, value_states


class DecoderOnlyFlashAttention:
    def forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_value: Optional[RebelDynamicCache] = None,
        batch_index: Optional[torch.Tensor] = None,
        output_attentions: bool = False,
        cos: Optional[torch.Tensor] = None,
        sin: Optional[torch.Tensor] = None,
        cache_pos_for_partitions: Optional[torch.Tensor] = None,
        kvcache_partition_size: Optional[torch.Tensor] = None,
        **kwargs,
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor], Optional[Tuple[torch.Tensor]]]:
        bsz, q_len, _ = hidden_states.size()
        query_states = self.q_proj(hidden_states)
        key_states = self.k_proj(hidden_states)
        value_states = self.v_proj(hidden_states)

        query_states = query_states.view(bsz, q_len, self.num_heads, self.head_dim).transpose(1, 2)
        key_states = key_states.view(bsz, q_len, self.num_key_value_heads, self.head_dim).transpose(1, 2)
        value_states = value_states.view(bsz, q_len, self.num_key_value_heads, self.head_dim).transpose(1, 2)

        query_states, key_states = apply_rotary_pos_emb(query_states, key_states, cos, sin)

        # Decoder (bsz > 1)
        if bsz > 1:
            all_key_states = []
            all_value_states = []
            all_attn_output = []

            for b in range(bsz):
                query_state = query_states[b].unsqueeze(0)
                attn_mask = attention_mask[b].unsqueeze(0)
                key_state = key_states[b].unsqueeze(0)
                value_state = value_states[b].unsqueeze(0)

                # reshape for removing repeat_kv (batch=1 , num_head, 1, q_len=1, head_dim)
                key_state = key_state.unsqueeze(2)
                value_state = value_state.unsqueeze(2)
                attn_mask = attn_mask.unsqueeze(2)

                query_state = query_state.view(
                    1,
                    self.num_key_value_heads,
                    self.num_heads // self.num_key_value_heads,
                    q_len,
                    self.head_dim,
                )

                # RBLN custom flash attention(decode), dummy batch index
                sidx = cache_pos_for_partitions[b][0]
                attn_output, key_state, value_state = torch.ops.rbln_custom_ops.flash_attn_decode(
                    query_state,
                    key_state,
                    value_state,
                    attn_mask,
                    past_key_value.key_cache[self.layer_idx].unsqueeze(2),
                    past_key_value.value_cache[self.layer_idx].unsqueeze(2),
                    sidx,
                    kvcache_partition_size,
                )

                # reshape for removing repeat_kv
                attn_output = attn_output.view(1, self.num_heads, q_len, self.head_dim)
                attn_output = attn_output.transpose(1, 2).contiguous()
                attn_output = attn_output.reshape(1, q_len, self.num_heads * self.head_dim)

                all_key_states.append(key_state)
                all_value_states.append(value_state)
                all_attn_output.append(attn_output)

            key_states = torch.cat(all_key_states, dim=0)
            value_states = torch.cat(all_value_states, dim=0)
            attn_output = torch.cat(all_attn_output, dim=0)

        else:
            # reshape for removing repeat_kv
            key_states = key_states.unsqueeze(2)
            value_states = value_states.unsqueeze(2)
            attention_mask = attention_mask.unsqueeze(2)
            query_states = query_states.view(
                1,
                self.num_key_value_heads,
                self.num_heads // self.num_key_value_heads,
                q_len,
                self.head_dim,
            )

            assert batch_index.dim() == 0
            assert not output_attentions
            bidx = batch_index
            sidx = cache_pos_for_partitions[0][0]
            attn_output, key_states, value_states = torch.ops.rbln_custom_ops.flash_attn_prefill(
                query_states,
                key_states,
                value_states,
                attention_mask,
                past_key_value.key_cache[self.layer_idx].unsqueeze(2),
                past_key_value.value_cache[self.layer_idx].unsqueeze(2),
                bidx,
                sidx,
                kvcache_partition_size,
            )

            # reshape for removing repeat_kv
            attn_output = attn_output.view(1, self.num_heads, q_len, self.head_dim)
            attn_output = attn_output.transpose(1, 2).contiguous()
            attn_output = attn_output.reshape(bsz, q_len, self.num_heads * self.head_dim)

        attn_output = self.o_proj(attn_output)

        if not output_attentions:
            attn_weight = None

        return attn_output, attn_weight, key_states, value_states


DECODERONLY_ATTENTION_CLASSES = {
    "eager": DecoderOnlyAttention,
    "flash_attn_rbln": DecoderOnlyFlashAttention,
    # "sdpa": DecoderOnlySdpaAttention,
}


class DecoderOnlyWrapper(torch.nn.Module):
    def __init__(self, model, max_seq_len, kvcache_partition_len=None):
        super().__init__()
        self.config = model.config
        self.model = model.model
        self.lm_head = model.lm_head
        self.max_seq_len = max_seq_len
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

    def get_forward_dict(self):
        forward_dict = {
            "wrapper": DecoderOnlyModel.forward,
            "model": DecoderOnlyDecoderLayer.forward,
            "decoder_layer": DECODERONLY_ATTENTION_CLASSES[self.attn_implementation].forward,
        }
        return forward_dict

    def forward(
        self,
        input_ids_or_inputs_embeds,
        attention_mask,
        cache_position,
        batch_position,
        query_idx,
        *past_key_values,
    ):
        if input_ids_or_inputs_embeds.ndim == 2:
            # input_ids
            input_ids = input_ids_or_inputs_embeds
            inputs_embeds = None
        elif input_ids_or_inputs_embeds.ndim == 3:
            # inputs_embeds
            input_ids = None
            inputs_embeds = input_ids_or_inputs_embeds
        else:
            raise NotImplementedError(f"Unknown ndim of input : {input_ids_or_inputs_embeds.ndim}")

        # Formatting list of past_kv to DynamicCache class.
        past_key_values = RebelDynamicCache.from_input_format(
            cache_position,
            self.config.num_hidden_layers,
            *past_key_values,
        )

        batch_size = input_ids_or_inputs_embeds.size()[0]
        seq_len = input_ids_or_inputs_embeds.size()[1]

        if self.attn_implementation == "eager":
            cache_pos_for_partitions = None
        elif self.attn_implementation == "flash_attn_rbln":
            p_len = self.kvcache_partition_size.size()[0]
            num_partition = self.max_seq_len // p_len
            if self.max_seq_len % p_len > 0:
                raise ValueError(
                    f"The partition length({p_len}) must be exactly divisible by the max_seq_len({self.max_seq_len})."
                )
            cache_pos_for_partitions = torch.zeros((batch_size, num_partition), dtype=torch.int32)

            if batch_size > 1:  # decode
                for b_idx in range(batch_size):
                    decoding_step = cache_position[b_idx]
                    cache_pos = decoding_step
                    for p_idx in range(num_partition):
                        input_0 = torch.tensor(cache_pos - p_len * p_idx, dtype=torch.int32)
                        input_1 = torch.tensor(p_len, dtype=torch.int32)
                        min = torch.minimum(input_0, input_1)
                        cache_pos_for_partition = torch.maximum(min, torch.tensor(0, dtype=torch.int32))
                        cache_pos_for_partitions[b_idx][p_idx] = cache_pos_for_partition
            else:  # prefill
                cache_pos = cache_position[0][0]
                for p_idx in range(num_partition):
                    input_0 = torch.tensor(cache_pos - p_len * p_idx, dtype=torch.int32)
                    input_1 = torch.tensor(p_len, dtype=torch.int32)
                    min = torch.minimum(input_0, input_1)
                    cache_pos_for_partition = torch.maximum(min, torch.tensor(0, dtype=torch.int32))
                    cache_pos_for_partitions[0][p_idx] = cache_pos_for_partition
        else:
            raise NotImplementedError(f"Unknown attn_implementation: {self.attn_implementation}")

        forward_dict = self.get_forward_dict()
        outputs = forward_dict["wrapper"](
            self.model,
            input_ids=input_ids,
            inputs_embeds=inputs_embeds,
            attention_mask=attention_mask,
            position_ids=cache_position,
            past_key_values=past_key_values,
            batch_ids=batch_position,
            rotary_pos_emb=self.rotary_emb,
            cache_pos_for_partitions=cache_pos_for_partitions,
            kvcache_partition_size=self.kvcache_partition_size,
            forward_dict=forward_dict,
        )

        hidden_states = outputs[0]
        if seq_len != 1:
            hidden_states = hidden_states[:, query_idx.to(torch.int).unsqueeze(0)]

        logits = self.lm_head(hidden_states)

        output = (logits,) + outputs[1:]

        return output, batch_position + query_idx


class DecoderOnlyDecoderLayer:
    def forward(
        self,
        hidden_states: torch.Tensor,
        layer_idx: int,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_value: Optional[RebelDynamicCache] = None,
        output_attentions: Optional[bool] = None,
        use_cache: Optional[bool] = None,
        batch_ids: Optional[torch.Tensor] = None,
        cos: Optional[torch.Tensor] = None,
        sin: Optional[torch.Tensor] = None,
        cache_pos_for_partitions: Optional[torch.Tensor] = None,
        kvcache_partition_size: Optional[torch.Tensor] = None,
        forward_dict: Optional[Dict[str, classmethod]] = None,
        **kwargs,
    ) -> Tuple[torch.FloatTensor, Optional[Tuple[torch.FloatTensor, torch.FloatTensor]]]:
        residual = hidden_states

        hidden_states = self.input_layernorm(hidden_states)

        hidden_states, self_attn_weight, k, v = forward_dict["decoder_layer"](
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
            cache_pos_for_partitions=cache_pos_for_partitions,
            kvcache_partition_size=kvcache_partition_size,
            **kwargs,
        )
        past_key_value.assign(k, v, layer_idx)

        hidden_states = residual + hidden_states

        # Fully Connected
        residual = hidden_states
        hidden_states = self.post_attention_layernorm(hidden_states)
        hidden_states = self.mlp(hidden_states)
        hidden_states = residual + hidden_states

        outputs = (hidden_states,)

        if output_attentions:
            outputs += (self_attn_weight,)

        if use_cache:
            outputs += (past_key_value,)

        return outputs


class DecoderOnlyModel:
    def forward(
        self,
        input_ids: torch.LongTensor = None,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_values: Optional[RebelDynamicCache] = None,
        batch_ids: Optional[torch.Tensor] = None,
        inputs_embeds: Optional[torch.FloatTensor] = None,
        use_cache: Optional[bool] = True,
        output_attentions: Optional[bool] = False,
        output_hidden_states: Optional[bool] = False,
        cache_pos_for_partitions: Optional[torch.Tensor] = None,
        kvcache_partition_size: Optional[torch.Tensor] = None,
        forward_dict: Optional[Dict[str, classmethod]] = None,
        rotary_pos_emb=None,
    ) -> BaseModelOutputWithPast:
        # retrieve input_ids and inputs_embeds
        if (input_ids is None) ^ (inputs_embeds is not None):
            raise ValueError(
                "You cannot specify both input_ids and inputs_embeds at the same time, and must specify either one"
            )

        # embed positions
        if inputs_embeds is None:
            inputs_embeds = self.embed_tokens(input_ids)

        hidden_states = inputs_embeds
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


def slice_and_unsqueeze_cos_sin(cos, sin, position_ids, unsqueeze_dim=1):
    """Slice cos[position_ids], sin[position_ids] vector for the query."""
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

    return cos, sin


def rotate_half(x):
    """Rotates half the hidden dims of the input."""
    x1 = x[..., : x.shape[-1] // 2]
    x2 = x[..., x.shape[-1] // 2 :]
    return torch.cat((-x2, x1), dim=-1)


def apply_rotary_pos_emb(q, k, cos, sin):
    """Applies Rotary Position Embedding to the query and key tensors."""

    q_embed = (q * cos) + (rotate_half(q) * sin)
    k_embed = (k * cos) + (rotate_half(k) * sin)
    return q_embed, k_embed


class RotaryEmbedding(nn.Module):
    """RotaryEmbedding extended with Dynamic NTK scaling. Credits to the Reddit users /u/bloc97 and /u/emozilla"""

    def __init__(
        self,
        config: PretrainedConfig,
        max_seq_len_cached: int,
    ):
        super().__init__()

        if hasattr(config, "rope_scaling") and config.rope_scaling is not None:
            rope_type = config.rope_scaling.get("rope_type", config.rope_scaling.get("type"))
        else:
            rope_type = "default"

        inv_freq, attention_scaling = ROPE_INIT_FUNCTIONS[rope_type](config, max_seq_len_cached)
        position_ids = torch.arange(0, max_seq_len_cached, dtype=torch.float32)
        position_ids_expanded = position_ids[:, None]

        if rope_type == "dynamic":
            freqs = position_ids_expanded.float() * inv_freq.float()
        else:
            inv_freq_expanded = inv_freq[None, :]
            freqs = position_ids_expanded.float() @ inv_freq_expanded.float()

        emb = torch.cat((freqs, freqs), dim=-1)

        cos = emb.cos() * attention_scaling
        sin = emb.sin() * attention_scaling

        self.register_buffer("_cos_cached", cos, persistent=False)
        self.register_buffer("_sin_cached", sin, persistent=False)

    def forward(self, x, seq_len):
        return (
            self._cos_cached[:seq_len].to(dtype=x.dtype),
            self._sin_cached[:seq_len].to(dtype=x.dtype),
        )
