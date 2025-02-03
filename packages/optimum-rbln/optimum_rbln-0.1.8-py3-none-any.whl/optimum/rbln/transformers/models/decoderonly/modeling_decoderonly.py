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
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple, Union

import rebel  # noqa: F401
import torch  # noqa: F401
from transformers import AutoModelForCausalLM, PretrainedConfig, PreTrainedModel
from transformers.modeling_outputs import CausalLMOutputWithPast

from ....modeling_base import RBLNModel
from ....modeling_config import DEFAULT_COMPILED_MODEL_NAME, RBLNConfig, RBLNRuntimeConfig
from ....utils.runtime_utils import RBLNPytorchRuntime


logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from transformers import (
        AutoFeatureExtractor,
        AutoProcessor,
        AutoTokenizer,
        PretrainedConfig,
    )


class RBLNRuntimeModel(RBLNPytorchRuntime):
    mandatory_members = ["main_input_name"]


class RBLNDecoderOnlyModelForCausalLM(RBLNModel, ABC):
    """
    The DecoderOnly Model transformer with a language modeling head (linear layer) on top.
    This model inherits from [`RBLNMultiModel`]. Check the superclass documentation for the generic methods the library implements for all its models.

    A class to convert and run pre-trained transformers based DecoderOnlyForCausalLM model on RBLN devices.
    It implements the methods to convert a pre-trained transformers DecoderOnlyForCausalLM model into a RBLN transformer model by:
    - transferring the checkpoint weights of the original into an optimized RBLN graph,
    - compiling the resulting graph using the RBLN compiler.
    """

    main_input_name = "input_ids"
    auto_model_class = AutoModelForCausalLM

    def __post_init__(self, **kwargs):
        self.batch_size = self.rbln_config.meta["rbln_batch_size"]
        self.max_seq_len = self.rbln_config.meta["rbln_max_seq_len"]
        self.prefill_chunk_size = self.rbln_config.meta["rbln_prefill_chunk_size"]

        self.prefill_attention_mask = torch.zeros(1, 1, self.prefill_chunk_size, self.max_seq_len, dtype=torch.int64)
        self.causal_mask = 1 - torch.triu(
            torch.ones(1, 1, self.prefill_chunk_size, self.prefill_chunk_size), diagonal=1
        )
        self.dec_attn_mask_init = torch.zeros(1, 1, 1, self.max_seq_len, dtype=torch.int64)
        self.dec_attn_mask = torch.zeros(self.batch_size, 1, 1, self.max_seq_len, dtype=torch.int64)
        self.prefill_decoder = RBLNRuntimeModel(runtime=self.model[0], main_input_name="input_ids")
        self.decoder = RBLNRuntimeModel(runtime=self.model[1], main_input_name="input_ids")

    @classmethod
    @abstractmethod
    def wrapping_torch_model(self, model: "PreTrainedModel", rbln_max_seq_len: int):
        pass

    @classmethod
    @torch.inference_mode()
    def get_compiled_model(cls, model: "PreTrainedModel", rbln_config: RBLNConfig):
        wrapped_model = cls.wrapping_torch_model(model, rbln_config.meta["rbln_max_seq_len"])

        prefill_rbln_runtime_config = rbln_config[DEFAULT_COMPILED_MODEL_NAME][0]
        dec_rbln_runtime_config = rbln_config[DEFAULT_COMPILED_MODEL_NAME][1]

        prefill_example_inputs = prefill_rbln_runtime_config.get_dummy_inputs(fill=0)
        dec_example_inputs = dec_rbln_runtime_config.get_dummy_inputs(fill=4)

        batch_index = 3
        dec_example_inputs[batch_index].fill_(-1)  # fill batch_position -1 to indicate it is decoder.

        prefill_scripted_model = torch.jit.trace(wrapped_model, prefill_example_inputs, check_trace=False)
        dec_scripted_model = torch.jit.trace(wrapped_model, dec_example_inputs, check_trace=False)

        prefill_ir = rebel.torchscript_to_ir(
            prefill_scripted_model,
            input_names=[v[0] for v in prefill_rbln_runtime_config.input_info],
        )
        dec_ir = rebel.torchscript_to_ir(
            dec_scripted_model,
            input_names=[v[0] for v in dec_rbln_runtime_config.input_info],
        )

        # Caching prefill_decoder/decoder I/O
        cache_index_offset = 4
        connections = [
            (prefill_ir.outputs[1 + i], prefill_ir.inputs[cache_index_offset + i])
            for i in range(model.config.num_hidden_layers * 2)
        ]

        compiled_model = rebel.compile(
            prefill_ir,
            dec_ir,
            connections=connections,
            fusion=prefill_rbln_runtime_config.fusion,
            npu=prefill_rbln_runtime_config.npu,
            tensor_parallel_size=prefill_rbln_runtime_config.tensor_parallel_size,
            use_weight_sharing=True,
        )
        return compiled_model

    @classmethod
    def _get_rbln_config(
        cls,
        preprocessors: Union["AutoFeatureExtractor", "AutoProcessor", "AutoTokenizer"],
        model_config: "PretrainedConfig",
        rbln_max_seq_len: Optional[int] = None,
        rbln_batch_size: Optional[int] = None,
        **kwargs,
    ) -> RBLNConfig:
        meta = {}

        prefill_chunk_size = 128
        if rbln_max_seq_len is None:
            rbln_max_seq_len = getattr(model_config, "max_position_embeddings", None)
        rbln_batch_size = 1 if rbln_batch_size is None else rbln_batch_size

        meta["rbln_max_seq_len"] = rbln_max_seq_len
        meta["rbln_batch_size"] = rbln_batch_size
        meta["rbln_prefill_chunk_size"] = prefill_chunk_size

        def get_input_info(
            batch_size,
            query_length,
        ):
            head_dim = (
                model_config.head_dim
                if hasattr(model_config, "head_dim")
                else model_config.hidden_size // model_config.num_attention_heads
            )
            input_info = [
                ("input_ids", [batch_size, query_length], "int64"),
                ("attention_mask", [batch_size, 1, query_length, rbln_max_seq_len], "int64"),
                (
                    "cache_position",
                    [batch_size, query_length],
                    "int32",
                ),
                ("batch_position", [], "int16"),
            ]

            input_info.extend(
                [
                    (
                        f"past_key_values_{i}",
                        [
                            rbln_batch_size,
                            model_config.num_key_value_heads,
                            rbln_max_seq_len,
                            head_dim,
                        ],
                        "float32",
                    )
                    for i in range(model_config.num_hidden_layers * 2)
                ]
            )

            return input_info

        prefill_input_info = get_input_info(
            batch_size=1,
            query_length=prefill_chunk_size,
        )
        dec_input_info = get_input_info(
            batch_size=rbln_batch_size,
            query_length=1,
        )

        prefill_rbln_runtime_config = RBLNRuntimeConfig(input_info=prefill_input_info)
        dec_rbln_runtime_config = RBLNRuntimeConfig(input_info=dec_input_info)

        dec_rbln_runtime_config.batch_size = rbln_batch_size

        rbln_config = RBLNConfig.from_rbln_runtime_configs(
            [prefill_rbln_runtime_config, dec_rbln_runtime_config],
            _rbln_meta=meta,
        )

        return rbln_config

    @classmethod
    def _create_runtimes(
        cls, compiled_models: List[rebel.RBLNCompiledModel], rbln_device_map: Dict[str, int]
    ) -> List[rebel.Runtime]:
        device_val = rbln_device_map[DEFAULT_COMPILED_MODEL_NAME]
        return [
            compiled_models[0].create_runtime(input_info_index=0, tensor_type="pt", device=device_val),
            compiled_models[0].create_runtime(input_info_index=1, tensor_type="pt", device=device_val),
        ]

    def get_decoder(self):
        return self.decoder

    def can_generate(self):
        return True

    def _reorder_cache(self, past_key_values, beam_idx):
        raise NotImplementedError

    # args input_ids, past_key_values and attention_mask are updated by _update_model_kwargs_for_generation() in _greedy_search() in GenerationMixin
    def prepare_inputs_for_generation(self, input_ids, past_key_values=None, attention_mask=None, **kwargs):
        batch_size = input_ids.shape[0]

        # FIXME past_key_values is just carriier variable for past_cached_length
        # torch.tensor((4,1),dtype=torch.int32) which refers a past_cached_length of each batch
        past_cached_length = past_key_values
        if past_cached_length is None:
            l_input_ids = []
            cache_positions = []
            past_cached_length = torch.zeros((batch_size, 1), dtype=torch.int32)
            for i in range(batch_size):
                input_id = input_ids[i]
                input_id = input_id[attention_mask[i] == 1]
                valid_len = input_id.shape[-1]
                cache_position = torch.arange(0, valid_len, dtype=torch.int32)
                past_cached_length[i] = valid_len
                l_input_ids.append(input_id.unsqueeze(0))
                cache_positions.append(cache_position.unsqueeze(0))

            input_ids = l_input_ids
        else:
            input_ids = input_ids[:, -1:]
            cache_positions = past_cached_length
            past_cached_length = past_cached_length + 1

        model_inputs = {
            "input_ids": input_ids,
            "cache_position": cache_positions,
            "past_cached_length": past_cached_length,
        }

        return model_inputs

    def forward(
        self,
        input_ids: torch.LongTensor = None,
        cache_position: Union[List[torch.Tensor], torch.Tensor] = None,  # vllm keyword argument
        batch_idx: Optional[int] = None,
        past_cached_length: Optional[torch.Tensor] = None,  # past_cached_length
        **kwargs,
    ) -> Tuple[torch.FloatTensor]:
        # prefll & hf generate
        if isinstance(cache_position, list):
            logits = []
            for batch_idx, (input_id, cache_pos) in enumerate(zip(input_ids, cache_position)):
                logit = self._forward_prefill(input_ids=input_id, cache_position=cache_pos, batch_idx=batch_idx)
                logits.append(logit)
            logits = torch.cat(logits, dim=0)
        # prefill & vllm step
        elif cache_position.shape[-1] > 1:
            logits = self._forward_prefill(input_ids=input_ids, cache_position=cache_position, batch_idx=batch_idx)
        # common decoder
        else:
            logits = self._forward_decoder(input_ids=input_ids, cache_position=cache_position)

        return CausalLMOutputWithPast(
            logits=logits,
            past_key_values=past_cached_length,  # past_cached_length
        )

    def _forward_prefill(
        self,
        input_ids: torch.LongTensor = None,
        cache_position: torch.Tensor = None,  # torch.tensor(,dtype=int32) (1,64) // (4,1)
        batch_idx: int = None,
    ) -> torch.FloatTensor:
        if batch_idx is None or batch_idx >= self.batch_size:
            raise RuntimeError(
                f"Invalid batch_idx ({batch_idx}). It must be a non-null value less than the batch size ({self.batch_size})."
            )
        query_length = input_ids.shape[1]
        attention_mask = self.prefill_attention_mask.clone()
        for step in range(0, query_length, self.prefill_chunk_size):
            if step + self.prefill_chunk_size > query_length:
                input_ids = torch.nn.functional.pad(input_ids, (0, step + self.prefill_chunk_size - query_length))
                cache_position = torch.cat(
                    [
                        cache_position,
                        torch.arange(
                            query_length,
                            step + self.prefill_chunk_size,
                            dtype=torch.int32,
                        ).unsqueeze(0),
                    ],
                    dim=-1,
                )

            sliced_input_ids = input_ids[:, step : step + self.prefill_chunk_size]
            sliced_cache_positions = cache_position[:, step : step + self.prefill_chunk_size]
            attention_mask[:, :, :, :step] = 1
            attention_mask[:, :, :, step : step + self.prefill_chunk_size] = self.causal_mask

            logits, _ = self.prefill_decoder(
                sliced_input_ids.contiguous(),
                attention_mask.contiguous(),
                sliced_cache_positions.contiguous(),
                torch.tensor(batch_idx, dtype=torch.int16),
            )
        logits = logits[:, query_length % self.prefill_chunk_size - 1].unsqueeze(1)

        self.dec_attn_mask[batch_idx] = self.dec_attn_mask_init.clone()
        self.dec_attn_mask[batch_idx, :, :, :query_length] = 1

        return logits

    def _forward_decoder(
        self, input_ids: torch.LongTensor = None, cache_position: torch.Tensor = None
    ) -> torch.FloatTensor:
        batch_size = input_ids.shape[0]

        for b_idx in range(batch_size):
            decoding_step = cache_position[b_idx].item()
            self.dec_attn_mask[b_idx, :, :, decoding_step] = 1

        logits, _ = self.decoder(
            input_ids.contiguous(),
            self.dec_attn_mask.contiguous(),
            cache_position.contiguous(),
            torch.tensor(0, dtype=torch.int16),
        )

        return logits
