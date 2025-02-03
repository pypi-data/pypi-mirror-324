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


from typing import Dict, Optional, Tuple, Union

import torch
import torch.nn as nn
from transformers.cache_utils import Cache, DynamicCache
from transformers.modeling_outputs import (
    BaseModelOutputWithPastAndCrossAttentions,
)

from .hf_hub_cached.modeling_midm import (
    MidmAttention,
    MidmBlock,
    MidmModel,
)


class _MidmRotaryEmbedding(nn.Module):
    """
    Implements Rotary Position Embedding from https://arxiv.org/abs/2104.09864.
    """

    def __init__(
        self, dim: int, seq_len_interpolation_factor: int = None, pretrained_max_position_embeddings: int = None
    ):
        """
        Args:

            dim (int): rotary embedding dimension
            seq_len_interpolation_factor (int): if not None, discrete positions will be interpolated
            by this factor via the trick in https://arxiv.org/abs/2306.15595.
            pretrained_max_position_embeddings (int): pre-trained max_position_embeddings before position interpolation.
        """
        super().__init__()
        self.seq_len_interpolation_factor = seq_len_interpolation_factor
        inv_freq = 1.0 / (10000 ** (torch.arange(0, dim, 2).float() / dim))
        self.register_buffer("inv_freq", inv_freq, persistent=False)
        self.pretrained_max_position_embeddings = pretrained_max_position_embeddings

        seq_len = pretrained_max_position_embeddings
        device = self.inv_freq.device
        dtype = torch.get_default_dtype()
        self.max_seq_len_cached = seq_len
        t = torch.arange(self.max_seq_len_cached, device=device, dtype=self.inv_freq.dtype)

        freqs = torch.outer(t, self.inv_freq)

        emb = torch.cat((freqs, freqs), dim=-1)
        self.register_buffer("emb_cached", emb.to(dtype), persistent=False)

    def forward(self, max_seq_len, offset=0):

        if max_seq_len > self.max_seq_len_cached:
            self._set_emb_cache(seq_len=max_seq_len)

        return self.emb_cached[:max_seq_len]


def _rotate_half(x):
    """
    change sign so the last dimension
    [A, B, C, D] -> [-C, -D, A, B]
    """
    x1 = x[..., : x.shape[-1] // 2]
    x2 = x[..., x.shape[-1] // 2 :]
    return torch.cat((-x2, x1), dim=-1)


def apply_rotary_pos_emb(t: torch.Tensor, cache_kwargs: Optional[Dict[str, torch.Tensor]] = None) -> torch.Tensor:
    """
    input tensor t is of shape [seq_length, ..., dim]
    rotary positional embeding tensor freqs is of shape [seq_length, ..., dim]
    check https://kexue.fm/archives/8265 for detailed formulas
    """

    freqs = cache_kwargs["rotary_pos_emb"]
    position_ids = cache_kwargs["position_ids"]
    unsqueeze_dim = 1

    rot_dim = freqs.shape[-1]

    t, t_pass = t[..., :rot_dim], t[..., rot_dim:]
    cos = freqs.cos()[position_ids].unsqueeze(unsqueeze_dim)
    sin = freqs.sin()[position_ids].unsqueeze(unsqueeze_dim)

    embed = (t * cos) + (_rotate_half(t) * sin)
    embed = torch.cat((embed, t_pass), dim=-1)

    return embed


class MidmLMHeadModelWrapper(torch.nn.Module):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.confg = model.config

        self.use_rotary_position_embedding = model.config.use_rotary_position_embedding
        if self.use_rotary_position_embedding:
            rotary_dim = model.config.hidden_size // model.config.num_attention_heads
            assert 0 < model.config.rotary_percentage <= 1
            if model.config.rotary_percentage < 1:
                rotary_dim = int(rotary_dim * model.config.rotary_percentage)
            self._rotary_pos_emb = _MidmRotaryEmbedding(
                rotary_dim,
                seq_len_interpolation_factor=None,
                pretrained_max_position_embeddings=model.config.max_position_embeddings,
            )

    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor,
        cache_position: torch.LongTensor,
        *past_key_values,
    ):
        past_kv_list = []
        for i in range(self.model.config.n_layer):
            cur_kv_layer = []
            for j in range(2):
                cur_kv_layer.append(past_key_values[2 * i + j])
            past_kv_list.append(cur_kv_layer)

        transformer_outputs = _MidmModel.forward(
            self.model.transformer,
            input_ids=input_ids,
            past_key_values=past_kv_list,
            attention_mask=attention_mask,
            position_ids=cache_position,
            rotary_pos_emb=self._rotary_pos_emb,
        )

        hidden_states = transformer_outputs[0]

        # For the input_ids, we assume right-alignment.
        # This assumption allows us to bypass dynamic indexing.
        hidden_states = hidden_states[:, -1:]
        lm_logits = self.model.lm_head(hidden_states)
        kv_cache = transformer_outputs[1]

        return lm_logits, kv_cache


def layernorm1p(module, input):
    return torch.nn.functional.layer_norm(input, module.normalized_shape, module.weight + 1, module.bias, module.eps)


class _MidmAttention(MidmAttention):
    def _attn(self, query, key, value, attention_mask=None, head_mask=None):
        attn_weights = torch.matmul(query, key.transpose(-1, -2))

        if self.scale_attn_weights:
            attn_weights = attn_weights / torch.full(
                [], value.size(-1) ** 0.5, dtype=attn_weights.dtype, device=attn_weights.device
            )

        if self.scale_attn_by_inverse_layer_idx or self.scale_qk_by_inverse_layer_idx:
            attn_weights = attn_weights / float(self.layer_idx + 1)

        if attention_mask is not None:
            attn_weights = attn_weights + attention_mask

        if self.scale_qk_by_inverse_layer_idx:
            attn_weights = attn_weights * float(self.layer_idx + 1)

        attn_weights = nn.functional.softmax(attn_weights, dim=-1)

        attn_weights = attn_weights.type(value.dtype)

        if head_mask is not None:
            attn_weights = attn_weights * head_mask

        attn_output = torch.matmul(attn_weights, value)

        return attn_output, attn_weights

    def forward(
        self,
        hidden_states: Optional[Tuple[torch.FloatTensor]],
        attention_mask: Optional[torch.FloatTensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_value: Optional[Cache] = None,
        head_mask: Optional[torch.FloatTensor] = None,
        use_cache: Optional[bool] = False,
        rotary_pos_emb=None,
    ) -> Tuple[Union[torch.Tensor, Tuple[torch.Tensor]], ...]:
        query, key, value = self.c_attn(hidden_states).split(self.split_size, dim=2)
        query = self._split_heads(query, self.num_heads, self.head_dim)
        key = self._split_heads(key, self.num_heads, self.head_dim)
        value = self._split_heads(value, self.num_heads, self.head_dim)

        kv_seq_len = key.shape[-2]
        if past_key_value is not None:
            if self.layer_idx is None:
                raise ValueError(
                    f"The cache structure has changed since version v4.36. If you are using {self.__class__.__name__} "
                    "for auto-regressive decoding with k/v caching, please make sure to initialize the attention class "
                    "with a layer index."
                )
            kv_seq_len += past_key_value.get_usable_length(kv_seq_len, self.layer_idx)

        if use_cache is True:
            present = (key, value)
        else:
            present = None

        if rotary_pos_emb is not None:
            query = apply_rotary_pos_emb(query, {"rotary_pos_emb": rotary_pos_emb, "position_ids": position_ids})
            key = apply_rotary_pos_emb(key, {"rotary_pos_emb": rotary_pos_emb, "position_ids": position_ids})

        if past_key_value is not None:
            key, value = past_key_value.update(key, value, self.layer_idx)

        attn_output, _ = _MidmAttention._attn(self, query, key, value, attention_mask, head_mask)

        attn_output = self._merge_heads(attn_output, self.num_heads, self.head_dim)

        attn_output = self.c_proj(attn_output)
        attn_output = self.resid_dropout(attn_output)

        outputs = (attn_output, present)

        return outputs, past_key_value


class _MidmBlock(MidmBlock):
    def forward(
        self,
        hidden_states: Optional[Tuple[torch.FloatTensor]],
        attention_mask: Optional[torch.FloatTensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_value: Optional[Tuple[torch.Tensor]] = None,
        head_mask: Optional[torch.FloatTensor] = None,
        use_cache: Optional[bool] = False,
        rotary_pos_emb=None,
    ) -> Union[Tuple[torch.Tensor], Optional[Tuple[torch.Tensor, Tuple[torch.FloatTensor, ...]]]]:
        residual = hidden_states
        if self.use_layernorm1p:
            hidden_states = layernorm1p(self.ln_1, hidden_states)
        else:
            hidden_states = self.ln_1(hidden_states)

        attn_outputs, present_key_value = _MidmAttention.forward(
            self.attn,
            hidden_states,
            attention_mask=attention_mask,
            position_ids=position_ids,
            past_key_value=past_key_value,
            head_mask=head_mask,
            rotary_pos_emb=rotary_pos_emb,
            use_cache=use_cache,
        )

        attn_output = attn_outputs[0]
        outputs = attn_outputs[1:]

        hidden_states = attn_output + residual

        residual = hidden_states
        if self.use_layernorm1p:
            hidden_states = layernorm1p(self.ln_2, hidden_states)
        else:
            hidden_states = self.ln_2(hidden_states)
        feed_forward_hidden_states = self.mlp(hidden_states)

        hidden_states = residual + feed_forward_hidden_states

        if use_cache:
            outputs = (hidden_states,) + outputs
        else:
            outputs = (hidden_states,) + outputs[1:]

        if use_cache:
            outputs += (present_key_value,)

        return outputs


class _MidmModel(MidmModel):
    def forward(
        self,
        input_ids: Optional[torch.LongTensor] = None,
        past_key_values: Optional[Tuple[Tuple[torch.Tensor]]] = None,
        attention_mask: Optional[torch.FloatTensor] = None,
        token_type_ids=None,
        position_ids: Optional[torch.LongTensor] = None,
        rotary_pos_emb=None,
        head_mask: Optional[torch.FloatTensor] = None,
        inputs_embeds=None,
        use_cache: Optional[bool] = None,
    ) -> Union[Tuple, BaseModelOutputWithPastAndCrossAttentions]:
        input_shape = input_ids.size()

        use_cache = use_cache if use_cache is not None else self.config.use_cache

        current_step = position_ids

        if input_ids is not None and inputs_embeds is not None:
            raise ValueError("You cannot specify both input_ids and inputs_embeds at the same time")
        elif input_ids is not None:
            batch_size, seq_length = input_ids.shape[:2]
        elif inputs_embeds is not None:
            batch_size, seq_length = inputs_embeds.shape[:2]
        else:
            raise ValueError("You have to specify either input_ids or inputs_embeds")

        if token_type_ids is not None:
            token_type_ids = token_type_ids.view(-1, input_shape[-1])

        past_key_values_length = 0

        if use_cache:
            use_legacy_cache = not isinstance(past_key_values, Cache)
            if use_legacy_cache:
                past_key_values = RebelDynamicCache.from_legacy_cache(
                    current_step=current_step,
                    max_length=self.config.max_position_embeddings,
                    past_key_values=past_key_values,
                )

        position_ids = torch.arange(0, input_ids.shape[-1], dtype=torch.int32).unsqueeze(0) + current_step

        if position_ids is None:
            device = input_ids.device if input_ids is not None else inputs_embeds.device
            position_ids = torch.arange(
                past_key_values_length, seq_length + past_key_values_length, dtype=torch.long, device=device
            )
            position_ids = position_ids.unsqueeze(0)

        attention_mask = (1.0 - attention_mask) * -10000.0

        if self.use_rotary_position_embedding:
            rotary_pos_emb = rotary_pos_emb(self.config.max_position_embeddings)

        head_mask = self.get_head_mask(head_mask, self.config.n_layer)

        if inputs_embeds is None:
            inputs_embeds = self.wte(input_ids)
        hidden_states = inputs_embeds

        if token_type_ids is not None:
            token_type_embeds = self.wte(token_type_ids)
            hidden_states = hidden_states + token_type_embeds

        hidden_states = self.drop(hidden_states)

        output_shape = (-1,) + input_shape[1:] + (hidden_states.size(-1),)

        next_decoder_cache = () if use_cache else None

        for i, (block, _) in enumerate(zip(self.h, past_key_values)):
            outputs = _MidmBlock.forward(
                block,
                hidden_states,
                attention_mask=attention_mask,
                position_ids=position_ids,
                past_key_value=past_key_values,
                head_mask=head_mask[i],
                rotary_pos_emb=rotary_pos_emb,
                use_cache=use_cache,
            )
            hidden_states = outputs[0]

            if use_cache:
                next_decoder_cache = outputs[2]

        if self.use_layernorm1p:
            hidden_states = layernorm1p(self.ln_f, hidden_states)
        else:
            hidden_states = self.ln_f(hidden_states)
        hidden_states = hidden_states.view(output_shape)

        next_cache = None
        if use_cache:
            next_cache = next_decoder_cache.to_legacy_cache() if use_legacy_cache else next_decoder_cache

        # return BaseModelOutputWithPast(last_hidden_state=hidden_states, past_key_values=next_cache)
        return hidden_states, next_cache


class RebelDynamicCache(DynamicCache):
    """
    A cache that grows dynamically as more tokens are generated. This is the default for generative models.

    It stores the Key and Value states as a list of tensors, one for each layer. The expected shape for each tensor is
    `[batch_size, num_heads, seq_len, head_dim]`.
    """

    def __init__(self, current_step, max_length) -> None:
        super().__init__()
        self.current_step = current_step
        self.max_length = max_length

    def copy(
        self,
        key_states: torch.Tensor,
        value_states: torch.Tensor,
        layer_idx: int,
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
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Updates the cache with the new `key_states` and `value_states` for the layer `layer_idx`
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

        if len(self.key_cache) <= layer_idx:
            self.key_cache.append(key_states)
            self.value_cache.append(value_states)
        else:
            self.key_cache[layer_idx] = self.key_cache[layer_idx].slice_scatter(
                key_states, dim=2, start=self.current_step, end=self.current_step + key_states.shape[2]
            )
            self.value_cache[layer_idx] = self.value_cache[layer_idx].slice_scatter(
                value_states, dim=2, start=self.current_step, end=self.current_step + value_states.shape[2]
            )

        return self.key_cache[layer_idx], self.value_cache[layer_idx]

    def get_seq_length(self, layer_idx: Optional[int] = 0) -> int:
        """Returns the sequence length of the cached states. A layer index can be optionally passed."""
        if len(self.key_cache) <= layer_idx:
            return 0
        return self.key_cache[layer_idx].shape[-2]

    def get_max_length(self) -> Optional[int]:
        return self.max_length

    @classmethod
    def from_legacy_cache(
        cls, current_step, max_length, past_key_values: Optional[Tuple[Tuple[torch.FloatTensor]]] = None
    ) -> "DynamicCache":
        """Converts a cache in the legacy cache format into an equivalent `DynamicCache`."""
        cache = cls(current_step, max_length)
        if past_key_values is not None:
            for layer_idx in range(len(past_key_values)):
                key_states, value_states = past_key_values[layer_idx]
                cache.copy(key_states, value_states, layer_idx)
        return cache
