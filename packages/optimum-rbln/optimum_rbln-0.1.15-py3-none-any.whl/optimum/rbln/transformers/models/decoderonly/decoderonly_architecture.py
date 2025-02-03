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
from typing import List, Optional, Tuple

import torch
from torch import nn
from transformers import PretrainedConfig, PreTrainedModel
from transformers.pytorch_utils import is_torch_greater_or_equal_than_2_4

from ....utils import logging
from ...modeling_rope_utils import ROPE_INIT_FUNCTIONS


if is_torch_greater_or_equal_than_2_4:
    register_fake = torch.library.register_fake
else:
    register_fake = torch.library.impl_abstract


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


@register_fake("rbln_custom_ops::flash_attn_decode")
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


@register_fake("rbln_custom_ops::flash_attn_prefill")
def flash_attn_prefill_abstract(q, k, v, m, kcache, vcache, batch, seq, partition):
    return torch.empty_like(q), torch.empty_like(kcache), torch.empty_like(vcache)


# RBLN custom op(cache update)
torch.library.define("rbln_custom_ops::rbln_cache_update", "(Tensor x, Tensor y, Tensor z, Tensor w) -> Tensor")


@torch.library.impl("rbln_custom_ops::rbln_cache_update", "cpu")
def rbln_cache_update_cpu(cache, value, batch, seq):
    updated_cache = cache[batch].slice_scatter(value, dim=-2, start=batch[0], end=batch[0] + seq[0])
    return updated_cache


@register_fake("rbln_custom_ops::rbln_cache_update")
def rbln_cache_update_abstract(cache, value, batch, seq):
    return torch.empty_like(cache)


class DecoderOnlyWrapper(nn.Module):
    """A wrapper class for decoder-only language models that handles RBLN-specific optimizations and requirements.

    This wrapper is designed to:
    1. Convert Huggingface decoder models for RBLN compilation with static shapes
    2. Handle input/model mapping and additional information supply (e.g., positional embeddings)
    3. Manage different attention implementations (standard and flash attention)
    4. Support both prefill and decode phases

    Notes:
    - Wrapper must only receive positional arguments in forward() due to torch.jit.trace dependency
    - Wrapper should not contain neural network graph operations (including memory view handling)

    Args:
        causal_lm (PreTrainedModel): The Huggingface causal language model to wrap
        max_seq_len (int): Maximum sequence length for position embeddings and cache sizes
        use_rotary_emb (bool): Whether to use rotary position embeddings
        kvcache_partition_len (Optional[int]): Length of KV cache partitions for flash attention.
            If provided, uses flash attention; if None, uses standard attention
    """

    def __init__(self, causal_lm: PreTrainedModel, max_seq_len, use_rotary_emb: bool, kvcache_partition_len=None):
        super().__init__()
        self.config = causal_lm.config

        if use_rotary_emb:
            self.rotary_emb = self.get_rotary_emb(max_seq_len=max_seq_len)
        else:
            self.rotary_emb = None

        if kvcache_partition_len is not None:
            # WORKAROUND : for passing partition length as a value to the rbln compiler.
            # What is actually used is the shape of this tensor.
            self.attn_impl = "flash_attn"
            logger.info(f"Using flash-attention. (partition length : {kvcache_partition_len})")
        else:
            self.attn_impl = "eager"
        self.kvcache_partition_len = kvcache_partition_len

        self.causal_lm = self.convert_to_rbln_causal_lm(causal_lm)

        self.num_hidden_layers = getattr(self.config, "num_hidden_layers", None) or getattr(self.config, "n_layer")
        self._phase = "prefill"

    def get_rotary_emb(self, max_seq_len):
        return RotaryEmbedding(config=self.config, max_seq_len_cached=max_seq_len)

    def convert_to_rbln_causal_lm(self, causal_lm: PreTrainedModel):
        new_layers = []
        for layer in causal_lm.model.layers:
            if self.attn_impl == "eager":
                new_self_attn = DecoderOnlyAttention(layer.self_attn)
            elif self.attn_impl == "flash_attn":
                new_self_attn = DecoderOnlyFlashAttention(
                    layer.self_attn, kvcache_partition_len=self.kvcache_partition_len
                )
            else:
                raise NotImplementedError(f"Unknwon attn : {self.attn_impl}")

            new_layer = DecoderOnlyLayer(layer, new_self_attn)
            new_layers.append(new_layer)
        new_model = DecoderOnlyModel(causal_lm.model, new_layers)
        new_causal_lm = DecoderOnlyForCausalLM(causal_lm, new_model)
        return new_causal_lm

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, phase: str):
        self._phase = phase
        self.causal_lm.phase = phase

    def forward(
        self,
        input_ids_or_inputs_embeds,
        attention_mask,
        cache_position,
        batch_position,
        query_position,
        *past_key_values,
    ):
        if input_ids_or_inputs_embeds.ndim == 2:
            # It is input_ids
            input_ids = input_ids_or_inputs_embeds
            inputs_embeds = None
        elif input_ids_or_inputs_embeds.ndim == 3:
            # It is inputs_embeds
            input_ids = None
            inputs_embeds = input_ids_or_inputs_embeds
        else:
            raise NotImplementedError(f"Unknown ndim of input : {input_ids_or_inputs_embeds.ndim}")

        if len(past_key_values) != 2 * self.num_hidden_layers:
            raise ValueError(
                f"Different past_key_values to model's config. {len(past_key_values)} != {self.num_hidden_layers}"
            )

        seq_len = input_ids_or_inputs_embeds.shape[1]
        if seq_len == 1:
            self.phase = "decode"
        else:
            self.phase = "prefill"

        # [key, value] * n_layer -> ( (key, value) ) * n_layer
        # cache shape : batch, n_heads, 1, max_seq_len, head_dim
        _past_key_values = []
        for i in range(self.config.num_hidden_layers):
            key_states = past_key_values[i * 2]
            value_states = past_key_values[i * 2 + 1]
            past_key_value = [key_states, value_states]
            _past_key_values.append(past_key_value)
        past_key_values = _past_key_values

        logit, present_key_values = self.causal_lm(
            input_ids=input_ids,
            inputs_embeds=inputs_embeds,
            attention_mask=attention_mask,
            cache_position=cache_position,
            batch_position=batch_position,
            query_position=query_position,
            past_key_values=past_key_values,
            rotary_emb=self.rotary_emb,
        )

        # ((key, value)) * n_layer -> [key, value] * n_layer
        _present_key_values = ()
        for i in range(self.num_hidden_layers):
            key_states = present_key_values[i][0]
            value_states = present_key_values[i][1]
            _present_key_values = _present_key_values + (key_states, value_states)
        present_key_values = _present_key_values

        # batch_position + query_position is dummy output node to keep the number of outputs
        return logit, present_key_values, batch_position + query_position


class DecoderOnlyForCausalLM(nn.Module):
    """A specialized wrapper for Causal Language Models optimized for RBLN compilation.

    This class adapts Huggingface's CausalLM (or similar models) for RBLN deployment by:
    1. Managing model phases (prefill/decode) throughout the computation graph
    2. Handling output shape alignments for static compilation
    3. Coordinating between the original model and RBLN-optimized components

    The class serves as an intermediate layer between DecoderOnlyWrapper and the core model,
    focusing on maintaining correct model behavior while enabling RBLN-specific optimizations.

    Args:
        causal_lm (PreTrainedModel): Original Huggingface causal language model
        model (DecoderOnlyModel): RBLN-optimized model instance

    Attributes:
        config: Configuration from the original causal language model
        _original_mod: Reference to the original model for components like lm_head
        model: RBLN-optimized decoder model instance
        _phase: Current processing phase ("prefill" or "decode")
    """

    def __init__(self, causal_lm: PreTrainedModel, model):
        super().__init__()
        self.config = causal_lm.config
        self._original_mod = causal_lm
        self.model = model
        self._phase = "prefill"

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, phase: str):
        self._phase = phase
        self.model.phase = phase

    def forward(
        self,
        input_ids: torch.Tensor = None,
        inputs_embeds: torch.Tensor = None,
        attention_mask: torch.Tensor = None,
        cache_position: torch.Tensor = None,
        batch_position: torch.Tensor = None,
        query_position: torch.Tensor = None,
        past_key_values: Tuple[Tuple[torch.Tensor]] = None,
        rotary_emb: nn.Module = None,
    ):
        # outputs
        hidden_states, present_key_values = self.model(
            input_ids=input_ids,
            inputs_embeds=inputs_embeds,
            attention_mask=attention_mask,
            cache_position=cache_position,
            batch_position=batch_position,
            past_key_values=past_key_values,
            rotary_emb=rotary_emb,
        )

        if self.phase == "prefill":
            hidden_states = hidden_states[:, query_position.to(torch.int).unsqueeze(0)]

        logits = self._original_mod.lm_head(hidden_states)
        output = (logits, present_key_values)
        return output


class DecoderOnlyModel(nn.Module):
    """A modified decoder-only model implementation optimized for RBLN compilation.

    Args:
        model: Original Huggingface model to adapt
        layers (List[DecoderOnlyLayer]): Modified transformer layers optimized for RBLN

    Attributes:
        _original_mod: Reference to original Huggingface model
        layers: ModuleList of RBLN-optimized transformer layers
        _phase: Current processing phase ("prefill" or "decode")
    """

    mask_fmin = torch.finfo(torch.float16).min

    def __init__(self, model, layers: List["DecoderOnlyLayer"]):
        super().__init__()
        self._original_mod = model
        self.layers = nn.ModuleList(layers)
        self._phase = "prefill"

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, phase: str):
        self._phase = phase
        for layer in self.layers:
            layer.phase = phase

    @property
    def hidden_multiplier(self):
        return 1

    def get_last_layernorm(self) -> nn.LayerNorm:
        return self._original_mod.norm

    def get_embedding(self) -> nn.Embedding:
        return self._original_mod.embed_tokens

    def get_pos_embedding(self) -> nn.Embedding:
        raise NotImplementedError(
            "The 'get_pos_embedding' method is not implemented. Please define this method in a subclass."
        )

    def forward(
        self,
        input_ids: torch.Tensor = None,
        inputs_embeds: torch.Tensor = None,
        attention_mask: torch.Tensor = None,
        cache_position: torch.Tensor = None,
        batch_position: torch.Tensor = None,
        past_key_values: Tuple[Tuple[torch.Tensor]] = None,
        rotary_emb: nn.Module = None,
    ):
        # retrieve input_ids and inputs_embeds
        if (input_ids is None) ^ (inputs_embeds is not None):
            raise ValueError(
                "You cannot specify both input_ids and inputs_embeds at the same time, and must specify either one"
            )

        # embed positions
        if inputs_embeds is None:
            inputs_embeds = self.get_embedding()(input_ids)

        hidden_states = inputs_embeds * self.hidden_multiplier
        attention_mask = (1 - attention_mask) * self.mask_fmin

        # get cos,sin vector if needed
        if rotary_emb is not None:
            cos, sin = rotary_emb(hidden_states, attention_mask.shape[-1])  # dtype carrier, max_seq_len
            cos, sin = slice_and_unsqueeze_cos_sin(cos, sin, cache_position)
        else:
            batch_size = inputs_embeds.shape[0]
            if cache_position.shape[0] > 1:
                position_embeds = []
                for b_idx in range(batch_size):
                    position_embed = self.get_pos_embedding()(cache_position[b_idx])
                    position_embeds.append(position_embed)

                position_embeds = torch.cat(position_embeds, dim=0).unsqueeze(1)
            else:
                position_embeds = self.get_pos_embedding()(cache_position)
            hidden_states = hidden_states + position_embeds
            cos, sin = None, None

        # (batch, seq_len) -> (batch,)
        current_steps = cache_position[:, 0]

        present_key_values = past_key_values
        for layer in self.layers:
            hidden_states, present_key_values = layer(
                hidden_states=hidden_states,
                attention_mask=attention_mask,
                current_steps=current_steps,
                batch_position=batch_position,
                past_key_values=present_key_values,
                cos=cos,
                sin=sin,
            )

        hidden_states = self.get_last_layernorm()(hidden_states)
        return hidden_states, present_key_values


class DecoderOnlyLayer(nn.Module):
    """A single transformer layer adapted for RBLN compilation with static shapes.

    This layer implements a modified transformer block that includes:
    1. Self-attention mechanism (either standard or flash attention)
    2. Feed-forward network (FFN)
    3. Layer normalization
    4. Residual connections

    The layer is specifically designed to:
    - Support compilation to RBLN custom ops
    - Maintain static tensor shapes throughout computations
    - Handle both prefill and decode phases efficiently
    - Manage attention state transitions properly

    Args:
        layer: Original transformer layer module to wrap
        self_attn (DecoderOnlyAttention): Modified attention module optimized for RBLN

    Attributes:
        _original_mod: Reference to original layer for accessing components
        self_attn: Modified attention mechanism mapped to RBLN ops at compile time
        phase: Current operation phase ("prefill" or "decode")
    """

    def __init__(self, layer, self_attn: "DecoderOnlyAttention"):
        super().__init__()
        self._original_mod = layer
        self.self_attn = self_attn
        self._phase = "prefill"

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, phase: str):
        self._phase = phase
        self.self_attn.phase = phase

    def get_pre_attention_layernorm(self) -> nn.LayerNorm:
        return self._original_mod.input_layernorm

    def get_post_attention_layernorm(self) -> nn.LayerNorm:
        return self._original_mod.post_attention_layernorm

    def forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: torch.Tensor,
        current_steps: torch.LongTensor,
        batch_position: torch.Tensor,
        past_key_values: Tuple[Tuple[torch.Tensor]],
        cos: Optional[torch.Tensor] = None,
        sin: Optional[torch.Tensor] = None,
    ):
        residual = hidden_states

        hidden_states = self.get_pre_attention_layernorm()(hidden_states)

        hidden_states, present_key_values = self.self_attn(
            hidden_states=hidden_states,
            attention_mask=attention_mask,
            current_steps=current_steps,
            batch_position=batch_position,
            past_key_values=past_key_values,
            cos=cos,
            sin=sin,
        )
        hidden_states = residual + hidden_states

        # Fully Connected
        residual = hidden_states
        hidden_states = self.get_post_attention_layernorm()(hidden_states)
        hidden_states = self._original_mod.mlp(hidden_states)
        hidden_states = residual + hidden_states

        return hidden_states, present_key_values


class DecoderOnlyAttention(nn.Module):
    """Attention implementation for decoder-only models optimized for RBLN compilation.

    This class implements a modified version of the standard attention mechanism that:
    1. Supports static shape requirements for RBLN compilation
    2. Handles explicit batch and position management

    Args:
        self_attn: Original attention module from the base model
    """

    def __init__(self, self_attn):
        super().__init__()
        self._original_mod = self_attn
        self.layer_idx = self_attn.layer_idx
        self.num_heads = self._original_mod.num_heads
        self.head_dim = self._original_mod.head_dim
        self.phase = "prefill"
        self.__post_init__()

    def __post_init__(self):
        self.q_proj = self._original_mod.q_proj
        self.k_proj = self._original_mod.k_proj
        self.v_proj = self._original_mod.v_proj
        self.o_proj = self._original_mod.o_proj
        self.num_key_value_heads = self._original_mod.num_key_value_heads

    def projection(self, hidden_states) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Projects input hidden states into query, key, and value representations.

        Args:
            hidden_states: Input tensor of shape [batch_size, seq_len, hidden_dim]

        Returns:
            Tuple of (query_states, key_states, value_states)
        """
        query_states = self.q_proj(hidden_states)
        key_states = self.k_proj(hidden_states)
        value_states = self.v_proj(hidden_states)
        return query_states, key_states, value_states

    def apply_rotary_pos_embed(self, query_states, key_states, cos, sin):
        return apply_rotary_pos_emb(query_states, key_states, cos, sin)

    def rbln_attention(
        self,
        query_state,
        key_state,
        value_state,
        attn_mask,
        batch_idx,
        past_key_state,
        past_value_state,
        current_step,
        # below are designed for Midm, GPT which requires to support scaling for attention weights
        # TODO(jongho): Merge and manage scales generally
        layer_idx=None,
        scale_attn_weights: bool = None,
        scale_attn_by_inverse_layer_idx: bool = None,
        scale_qk_by_inverse_layer_idx: bool = None,
    ):
        """Compute attention with static shapes and explicit cache management.

        Args:
            query_state: Query tensor [1, num_heads, 1, head_dim]
            key_state: Key tensor [1, num_heads, seq_len, head_dim]
            value_state: Value tensor [1, num_heads, seq_len, head_dim]
            attn_mask: Attention mask tensor
            batch_idx: Batch index for cache lookup
            past_key_state: Previous key cache states
            past_value_state: Previous value cache states
            current_step: Current position in sequence

        Returns:
            Tuple of (attention_output, key_state, value_state)
        """
        # Implementation details.
        # reshape for removing repeat_kv (batch=1 , num_head, 1, q_len=1, head_dim)
        key_state = key_state.unsqueeze(2)  # 1, 32, 1, 128, 128
        value_state = value_state.unsqueeze(2)
        attn_mask = attn_mask.unsqueeze(2)

        query_state = query_state.view(
            1,
            self.num_key_value_heads,
            self.num_heads // self.num_key_value_heads,
            -1,  # seq len
            self.head_dim,
        )  #

        kend = current_step + key_state.shape[-2]
        vend = current_step + value_state.shape[-2]

        key_state = (
            past_key_state[batch_idx]
            .unsqueeze(0)
            .unsqueeze(2)
            .slice_scatter(key_state, dim=-2, start=current_step, end=kend)
        )
        value_state = (
            past_value_state[batch_idx]
            .unsqueeze(0)
            .unsqueeze(2)
            .slice_scatter(value_state, dim=-2, start=current_step, end=vend)
        )

        attn_weight = torch.matmul(query_state, key_state.transpose(3, 4))
        attn_weight = attn_weight / math.sqrt(self.head_dim)

        if layer_idx is not None and (scale_attn_by_inverse_layer_idx or scale_qk_by_inverse_layer_idx):
            attn_weight = attn_weight / float(layer_idx + 1)

        attn_weight += attn_mask

        if layer_idx is not None and scale_qk_by_inverse_layer_idx:
            attn_weight = attn_weight * float(layer_idx + 1)

        attn_weight = nn.functional.softmax(attn_weight, dim=-1)

        attn_output = torch.matmul(attn_weight, value_state)

        attn_output = attn_output.view(1, self.num_heads, -1, self.head_dim)
        attn_output = attn_output.transpose(1, 2).contiguous()
        attn_output = attn_output.reshape(1, -1, self.num_heads * self.head_dim)

        return attn_output, key_state, value_state

    def forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: torch.Tensor,
        current_steps: torch.LongTensor,
        batch_position: torch.Tensor,
        past_key_values: Tuple[Tuple[torch.Tensor]],
        cos: Optional[torch.Tensor] = None,  # (batch, 1, prefill_size, head_dim)
        sin: Optional[torch.Tensor] = None,
    ):
        batch_size, query_length, _ = hidden_states.size()

        query_states, key_states, value_states = self.projection(hidden_states=hidden_states)

        query_states = query_states.view(batch_size, query_length, self.num_heads, self.head_dim).transpose(1, 2)
        key_states = key_states.view(batch_size, query_length, self.num_key_value_heads, self.head_dim).transpose(1, 2)
        value_states = value_states.view(batch_size, query_length, self.num_key_value_heads, self.head_dim).transpose(
            1, 2
        )
        # b, num_head, query, head_dim

        if cos is not None and sin is not None:
            query_states, key_states = self.apply_rotary_pos_embed(query_states, key_states, cos, sin)

        if batch_size > 1 and self.phase == "prefill":
            raise NotImplementedError(f"batch size should be 1 if prefill phase, but got {batch_size}.")

        _key_states = []
        _value_states = []
        _attn_outputs = []
        for b in range(batch_size):
            current_step = current_steps[b]
            attn_output, key_state, value_state = self.rbln_attention(
                query_states[b].unsqueeze(0),
                key_states[b].unsqueeze(0),
                value_states[b].unsqueeze(0),
                attention_mask[b].unsqueeze(0)
                if self.phase == "decode"
                else attention_mask,  # TODO(jongho): fix when msoftmax is supported
                past_key_state=past_key_values[self.layer_idx][0],
                past_value_state=past_key_values[self.layer_idx][1],
                batch_idx=b if self.phase == "decode" else batch_position,
                current_step=current_step,
            )
            _key_states.append(key_state)
            _value_states.append(value_state)
            _attn_outputs.append(attn_output)
        key_states = torch.cat(_key_states, dim=0)
        value_states = torch.cat(_value_states, dim=0)
        attn_outputs = torch.cat(_attn_outputs, dim=0)

        attn_outputs = self.o_proj(attn_outputs)
        past_key_values[self.layer_idx] = key_states, value_states
        return attn_outputs, past_key_values


def slice_and_unsqueeze_cos_sin(cos, sin, cache_position, unsqueeze_dim=1):
    """Slice cos[cache_position], sin[cache_position] vector for the query."""
    if cache_position.shape[0] > 1:
        cos_all = []
        sin_all = []
        for i in range(cache_position.shape[0]):
            cos_all.append(cos[cache_position[i : i + 1]].unsqueeze(unsqueeze_dim))
            sin_all.append(sin[cache_position[i : i + 1]].unsqueeze(unsqueeze_dim))
        cos = torch.cat(cos_all, dim=0)
        sin = torch.cat(sin_all, dim=0)
    else:
        cos = cos[cache_position].unsqueeze(unsqueeze_dim)
        sin = sin[cache_position].unsqueeze(unsqueeze_dim)

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


def apply_rotary_pos_emb_partial(query_states, key_states, cos, sin, ndim) -> Tuple[torch.Tensor, torch.Tensor]:
    # Partial rotary embedding
    query_rot, query_pass = (
        query_states[..., :ndim],
        query_states[..., ndim:],
    )
    key_rot, key_pass = (
        key_states[..., :ndim],
        key_states[..., ndim:],
    )

    # [batch_size, seq_length, num_heads, head_dim // config.partial_rotary_factor]
    query_rot, key_rot = apply_rotary_pos_emb(query_rot, key_rot, cos, sin)

    # [batch_size, seq_length, num_heads, head_dim]
    query_states = torch.cat((query_rot, query_pass), dim=-1)
    key_states = torch.cat((key_rot, key_pass), dim=-1)
    return query_states, key_states


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
        cache_position = torch.arange(0, max_seq_len_cached, dtype=torch.float32)
        cache_position_expanded = cache_position[:, None]

        if rope_type == "dynamic":
            freqs = cache_position_expanded.float() * inv_freq.float()
        else:
            inv_freq_expanded = inv_freq[None, :]
            freqs = cache_position_expanded.float() @ inv_freq_expanded.float()

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


class DecoderOnlyFlashAttention(DecoderOnlyAttention):
    def __init__(self, self_attn, kvcache_partition_len):
        super().__init__(self_attn=self_attn)
        self.kvcache_partition_size = torch.zeros(kvcache_partition_len, dtype=torch.int32)

    def get_cache_pos_for_partitions(self, current_steps, batch_size, max_seq_len):
        partition_len = self.kvcache_partition_size.size()[0]
        num_partition = max_seq_len // partition_len
        cache_pos_for_partitions = torch.zeros((batch_size, num_partition), dtype=torch.int32)
        if self.phase == "decode":
            for b_idx in range(batch_size):
                cache_pos = current_steps[b_idx]
                for p_idx in range(num_partition):
                    cache_pos_for_partitions[b_idx][p_idx] = torch.clamp(
                        cache_pos - partition_len * p_idx, 0, partition_len
                    )
        else:  # prefill
            cache_pos = current_steps[0]
            for p_idx in range(num_partition):
                cache_pos_for_partitions[0][p_idx] = torch.clamp(cache_pos - partition_len * p_idx, 0, partition_len)

        return cache_pos_for_partitions

    def rbln_flash_attention(
        self,
        query_state,
        key_state,
        value_state,
        attn_mask,
        batch_idx,
        past_key_state,
        past_value_state,
        cache_pos_for_partitions,
    ):
        # reshape for removing repeat_kv (batch=1 , num_head, 1, q_len=1, head_dim)
        key_state = key_state.unsqueeze(2)  # 1, 32, 1, 128, 128
        value_state = value_state.unsqueeze(2)
        attn_mask = attn_mask.unsqueeze(2)

        query_state = query_state.view(
            1,
            self.num_key_value_heads,
            self.num_heads // self.num_key_value_heads,
            -1,  # seq len
            self.head_dim,
        )

        # RBLN custom flash attention(decode), dummy batch index
        if self.phase == "decode":
            sidx = cache_pos_for_partitions[batch_idx][0]
            attn_output, key_state, value_state = torch.ops.rbln_custom_ops.flash_attn_decode(
                query_state,
                key_state,
                value_state,
                attn_mask,
                past_key_state.unsqueeze(2),
                past_value_state.unsqueeze(2),
                sidx,
                self.kvcache_partition_size,
            )
        else:
            sidx = cache_pos_for_partitions[0][0]
            attn_output, key_state, value_state = torch.ops.rbln_custom_ops.flash_attn_prefill(
                query_state,
                key_state,
                value_state,
                attn_mask,
                past_key_state.unsqueeze(2),
                past_value_state.unsqueeze(2),
                batch_idx,
                sidx,
                self.kvcache_partition_size,
            )

        # reshape for removing repeat_kv
        attn_output = attn_output.view(1, self.num_heads, -1, self.head_dim)
        attn_output = attn_output.transpose(1, 2).contiguous()
        attn_output = attn_output.reshape(1, -1, self.num_heads * self.head_dim)

        return attn_output, key_state, value_state

    def forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: torch.Tensor,
        current_steps: torch.LongTensor,
        batch_position: torch.Tensor,
        past_key_values: Tuple[Tuple[torch.Tensor]],
        cos: Optional[torch.Tensor] = None,
        sin: Optional[torch.Tensor] = None,
    ):
        batch_size, query_length, _ = hidden_states.size()

        query_states, key_states, value_states = self.projection(hidden_states=hidden_states)

        query_states = query_states.view(batch_size, query_length, self.num_heads, self.head_dim).transpose(1, 2)
        key_states = key_states.view(batch_size, query_length, self.num_key_value_heads, self.head_dim).transpose(1, 2)
        value_states = value_states.view(batch_size, query_length, self.num_key_value_heads, self.head_dim).transpose(
            1, 2
        )
        # b, num_head, query, head_dim

        max_seq_len = past_key_values[self.layer_idx][0].shape[-2]

        if cos is not None and sin is not None:
            query_states, key_states = self.apply_rotary_pos_embed(query_states, key_states, cos, sin)

        cache_pos_for_partitions = self.get_cache_pos_for_partitions(
            current_steps, batch_size=batch_size, max_seq_len=max_seq_len
        )  # batch_size, num_partitions

        _key_states = []
        _value_states = []
        _attn_outputs = []
        for b in range(batch_size):
            attn_output, key_state, value_state = self.rbln_flash_attention(
                query_states[b].unsqueeze(0),
                key_states[b].unsqueeze(0),
                value_states[b].unsqueeze(0),
                attention_mask[b].unsqueeze(0)
                if self.phase == "decode"
                else attention_mask,  # TODO(jongho): fix when msoftmax is supported
                past_key_state=past_key_values[self.layer_idx][0],
                past_value_state=past_key_values[self.layer_idx][1],
                batch_idx=b if self.phase == "decode" else batch_position,
                cache_pos_for_partitions=cache_pos_for_partitions,
            )
            _key_states.append(key_state)
            _value_states.append(value_state)
            _attn_outputs.append(attn_output)
        key_states = torch.cat(_key_states, dim=0)
        value_states = torch.cat(_value_states, dim=0)
        attn_outputs = torch.cat(_attn_outputs, dim=0)

        attn_outputs = self.o_proj(attn_outputs)
        past_key_values[self.layer_idx] = key_states, value_states
        return attn_outputs, past_key_values
