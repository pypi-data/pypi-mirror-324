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

import inspect  # noqa: I001
import logging
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Tuple, Union

import torch  # noqa: F401
import rebel  # noqa: F401

from transformers import AutoModelForCausalLM, LlamaForCausalLM, PreTrainedModel, PretrainedConfig, AutoConfig
from transformers.modeling_outputs import CausalLMOutputWithPast

from ...generation.utils import RBLNGenerationMixin
from ....modeling_base import RBLNModel
from ....modeling_config import DEFAULT_COMPILED_MODEL_NAME, RBLNConfig, RBLNRuntimeConfig
from ....utils.runtime_utils import RBLNPytorchRuntime


# FIXME:: Merge Two architecture Codes
from .llama_architecture import (
    LlamaWrapper,
    wrap_llama,
    unwrap_llama,
)

from .llama_architecture_cb import (
    LlamaDynamicBatchWrapper as LlamaWrapper_cb,
    wrap_llama as wrap_llama_cb,
)


logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from transformers import (
        AutoFeatureExtractor,
        AutoProcessor,
        AutoTokenizer,
        PretrainedConfig,
    )


SUPPORTED_BATCHING_MODES = ["static", "vllm"]


class RBLNRuntimeModel(RBLNPytorchRuntime):
    mandatory_members = ["main_input_name"]


class RBLNLlamaForCausalLM(RBLNModel, RBLNGenerationMixin):
    """
    The Llama Model transformer with a language modeling head (linear layer) on top.
    This model inherits from [`RBLNMultiModel`]. Check the superclass documentation for the generic methods the library implements for all its models.

    A class to convert and run pre-trained transformers based LlamaForCausalLM model on RBLN devices.
    It implements the methods to convert a pre-trained transformers LlamaForCausalLM model into a RBLN transformer model by:
    - transferring the checkpoint weights of the original into an optimized RBLN graph,
    - compiling the resulting graph using the RBLN compiler.
    """

    main_input_name = "input_ids"
    auto_model_class = AutoModelForCausalLM

    def __post_init__(self, **kwargs):
        self.batch_size = self.rbln_config.meta["rbln_batch_size"]
        self.max_seq_len = self.rbln_config.meta["rbln_max_seq_len"]
        self.prefill_chunk_size = self.rbln_config.meta["rbln_prefill_chunk_size"]
        self.use_continuous_batch = self.rbln_config.meta["rbln_batching"] == "vllm"

        prefill_batch_size = self.batch_size if not self.use_continuous_batch else 1
        self.prefill_attention_mask = torch.zeros(
            prefill_batch_size, 1, self.prefill_chunk_size, self.max_seq_len, dtype=torch.int64
        )
        self.causal_mask = 1 - torch.triu(
            torch.ones(prefill_batch_size, 1, self.prefill_chunk_size, self.prefill_chunk_size), diagonal=1
        )
        self.decoder_attention_mask = torch.zeros(self.batch_size, 1, 1, self.max_seq_len, dtype=torch.int64)

        self.prefill_decoder = RBLNRuntimeModel(runtime=self.model[0], main_input_name="input_ids")
        self.decoder = RBLNRuntimeModel(runtime=self.model[1], main_input_name="input_ids")
        self.past_cached_length = 0
        self.right_padding = True

    @classmethod
    def update_kwargs(cls, kwargs):
        """
        Update user-given kwargs to get proper pytorch model.

        For example, `torchscript`=True should be set because torch.jit
        does not support `transformers` output instances as module output;
        """
        kwargs.update(
            {
                "torchscript": True,
                "return_dict": False,
                "use_cache": True,
                "torch_dtype": torch.float32,
                "_attn_implementation": "eager",
            }
        )
        return kwargs

    @classmethod
    def get_pytorch_model(
        cls,
        model_id: str,
        use_auth_token: Optional[Union[bool, str]] = None,
        revision: Optional[str] = None,
        force_download: bool = False,
        cache_dir: Optional[str] = None,
        subfolder: str = "",
        local_files_only: bool = False,
        trust_remote_code: bool = False,
        rbln_config_kwargs: Optional[Dict[str, Any]] = None,
        rbln_constructor_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> PreTrainedModel:
        if rbln_max_seq_len := rbln_config_kwargs.get("rbln_max_seq_len", None):
            config = AutoConfig.from_pretrained(model_id)
            if hf_position_embedding := getattr(config, "max_position_embeddings", None):
                if hf_position_embedding < rbln_max_seq_len:
                    logger.warning(
                        f"`rbln_max_seq_len` is larger than original config({hf_position_embedding})."
                        "This may lead to incorrect inferences of the model."
                    )
            kwargs.update({"max_position_embeddings": rbln_max_seq_len})

        # FIXME :: This should be moved when wrapping removed.
        use_continuous_batch = rbln_config_kwargs.get("rbln_batching", "static") == "vllm"
        wrap_llama_cb() if use_continuous_batch else wrap_llama()

        model = super().get_pytorch_model(
            model_id=model_id,
            use_auth_token=use_auth_token,
            revision=revision,
            force_download=force_download,
            cache_dir=cache_dir,
            subfolder=subfolder,
            local_files_only=local_files_only,
            trust_remote_code=trust_remote_code,
            rbln_config_kwargs=rbln_config_kwargs,
            rbln_constructor_kwargs=rbln_constructor_kwargs,
            **kwargs,
        )

        unwrap_llama()

        return model

    @classmethod
    @torch.inference_mode()
    def get_compiled_model(cls, model: "PreTrainedModel", rbln_config: RBLNConfig):
        use_continuous_batch = rbln_config.meta["rbln_batching"] == "vllm"

        wrapper_cls = LlamaWrapper_cb if use_continuous_batch else LlamaWrapper

        wrapped_model = wrapper_cls(model).eval()

        prefill_rbln_runtime_config = rbln_config[DEFAULT_COMPILED_MODEL_NAME][0]
        dec_rbln_runtime_config = rbln_config[DEFAULT_COMPILED_MODEL_NAME][1]

        prefill_example_inputs = prefill_rbln_runtime_config.get_dummy_inputs(fill=0)
        dec_example_inputs = dec_rbln_runtime_config.get_dummy_inputs(fill=4)

        if use_continuous_batch:
            batch_index_index = 3
            dec_example_inputs[batch_index_index].fill_(-1)  # fill batch_position -1 to indicate it is decoder.

        wrap_llama_cb() if use_continuous_batch else wrap_llama()

        prefill_scripted_model = torch.jit.trace(wrapped_model, prefill_example_inputs, check_trace=False)
        dec_scripted_model = torch.jit.trace(wrapped_model, dec_example_inputs, check_trace=False)

        unwrap_llama()

        prefill_ir = rebel.torchscript_to_ir(
            prefill_scripted_model,
            input_names=[v[0] for v in prefill_rbln_runtime_config.input_info],
        )
        dec_ir = rebel.torchscript_to_ir(
            dec_scripted_model,
            input_names=[v[0] for v in dec_rbln_runtime_config.input_info],
        )

        # Caching prefill_decoder/decoder I/O
        cache_index_offset = 4 if use_continuous_batch else 3
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
        rbln_batching: Optional[str] = None,
    ) -> RBLNConfig:
        meta = {}

        prefill_chunk_size = 128
        if rbln_max_seq_len is None:
            rbln_max_seq_len = getattr(model_config, "max_position_embeddings", None)
        rbln_batch_size = 1 if rbln_batch_size is None else rbln_batch_size
        rbln_batching = "static" if rbln_batching is None else rbln_batching

        meta["rbln_max_seq_len"] = rbln_max_seq_len
        meta["rbln_batch_size"] = rbln_batch_size
        meta["rbln_prefill_chunk_size"] = prefill_chunk_size
        meta["rbln_batching"] = rbln_batching
        use_continuous_batching = meta["rbln_batching"] == "vllm"

        if rbln_batching not in SUPPORTED_BATCHING_MODES:
            raise ValueError(
                f'rbln_batching="{rbln_batching}" is not a supported batch mode, '
                f"Possible: {SUPPORTED_BATCHING_MODES}"
            )

        def get_input_info(
            batch_size,  # should be 1 if continous batch prefill
            query_length,
            continuous_batch=False,  # determines the shape of `cache position`
        ):
            input_info = [
                ("input_ids", [batch_size, query_length], "int64"),
                ("attention_mask", [batch_size, 1, query_length, rbln_max_seq_len], "int64"),
                (
                    "cache_position",
                    [batch_size, query_length] if continuous_batch else [],
                    "int32",
                ),
            ]

            if continuous_batch:
                input_info.append(("batch_position", [], "int16"))

            input_info.extend(
                [
                    (
                        f"past_key_values_{i}",
                        [
                            rbln_batch_size,
                            model_config.num_key_value_heads,
                            rbln_max_seq_len,
                            model_config.hidden_size // model_config.num_attention_heads,
                        ],
                        "float32",
                    )
                    for i in range(model_config.num_hidden_layers * 2)
                ]
            )

            return input_info

        prefill_input_info = get_input_info(
            batch_size=1 if use_continuous_batching else rbln_batch_size,
            query_length=prefill_chunk_size,
            continuous_batch=use_continuous_batching,
        )
        dec_input_info = get_input_info(
            batch_size=rbln_batch_size,
            query_length=1,
            continuous_batch=use_continuous_batching,
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

    def __getattr__(self, __name: str) -> Any:
        def redirect(func):
            return lambda *pargs, **kwargs: func(self, *pargs, **kwargs)

        val = getattr(LlamaForCausalLM, __name)

        if isinstance(val, Callable) and "self" in set(inspect.signature(val).parameters):
            return redirect(val)

        return val

    def _reorder_cache(self, past_key_values, beam_idx):
        raise NotImplementedError

    # args input_ids, past_key_values and attention_mask are updated by _update_model_kwargs_for_generation() in _greedy_search() in GenerationMixin
    def prepare_inputs_for_generation(self, input_ids, past_key_values=0, attention_mask=None, **kwargs):
        batch_size, cur_len = input_ids.shape
        past_cached_length = past_key_values

        # In greedy decoding
        if past_cached_length == 0:
            # padding with prefill_chunk_size
            # TODO left padding + left padding has issue on stoppingcriteria(max_len)
            if cur_len % self.prefill_chunk_size != 0:
                pad_len = self.prefill_chunk_size - cur_len % self.prefill_chunk_size
                input_ids = torch.nn.functional.pad(input_ids, (0, pad_len))

            # padding_side
            if batch_size > 1 and torch.all(attention_mask[..., -1] == 1):
                self.right_padding = False

            if self.right_padding:
                self.rightpad_max_len = cur_len
                prompt_min_len = torch.min(torch.sum(attention_mask, dim=-1))
                self.dummy_len = torch.sum(attention_mask, dim=-1) - prompt_min_len  # dummy_decoder generation length
                query_length = prompt_min_len.item()
            else:
                query_length = cur_len - past_cached_length
                self.prompt_length = query_length
                self.prompt_attn_mask = attention_mask.unsqueeze(1).unsqueeze(1).contiguous()

            attention_mask = self.prefill_attention_mask.clone()
            cache_position = torch.tensor(0, dtype=torch.int32)

        else:
            if self.right_padding:
                attention_mask = torch.zeros(batch_size, 1, 1, self.max_seq_len, dtype=torch.int64)
                attention_mask[:, :, :, : past_cached_length + 1] = 1
                input_ids = input_ids[:, past_cached_length : past_cached_length + 1].contiguous()
            else:
                attention_mask = torch.nn.functional.pad(attention_mask, (0, self.max_seq_len - cur_len))
                attention_mask = attention_mask.reshape(batch_size, 1, 1, -1).contiguous()
                input_ids = input_ids[:, -1:]

            cache_position = torch.tensor(past_cached_length, dtype=torch.int32)
            query_length = 1

        model_inputs = {
            "input_ids": input_ids,
            "past_key_values": past_key_values,
            "attention_mask": attention_mask,
            "cache_position": cache_position,
            "query_length": query_length,
        }

        return model_inputs

    def forward(self, *args, **kwargs):
        if self.use_continuous_batch:
            return self.forward_cb(*args, **kwargs)
        else:
            return self.forward_static(*args, **kwargs)

    def forward_static(
        self,
        input_ids: torch.LongTensor = None,
        attention_mask: Optional[torch.Tensor] = None,
        past_key_values: int = None,
        cache_position: Optional[torch.Tensor] = None,
        query_length: Optional[torch.Tensor] = None,
        **kwargs,
    ) -> Tuple[torch.FloatTensor]:
        if past_key_values is not None:
            past_key_values += query_length

        # prefill_decoder
        if cache_position == 0:
            for step in range(0, query_length, self.prefill_chunk_size):
                sliced_input_ids = input_ids[:, step : step + self.prefill_chunk_size]
                attention_mask[:, :, :, :step] = 1
                attention_mask[:, :, :, step : step + self.prefill_chunk_size] = self.causal_mask
                if not self.right_padding:
                    attention_mask[:, :, :, : self.prompt_length] &= self.prompt_attn_mask[:, :, :, :]

                outputs = self.prefill_decoder(
                    input_ids=sliced_input_ids.contiguous(),
                    attention_mask=attention_mask.contiguous(),
                    cache_position=cache_position + step,
                )
            outputs = outputs[:, query_length % self.prefill_chunk_size - 1].unsqueeze(1)

        # decoder
        else:
            outputs = self.decoder(
                input_ids.contiguous(),
                attention_mask.contiguous(),
                cache_position=cache_position,
            )

        return CausalLMOutputWithPast(
            logits=outputs,
            past_key_values=past_key_values,
        )

    def forward_cb(
        self,
        input_ids: torch.LongTensor = None,
        cache_position: Optional[torch.Tensor] = None,  # torch.tensor(,dtype=int32) (1,64) // (4,1)
        batch_idx: int = None,
        **kwargs,
    ) -> Tuple[torch.FloatTensor]:
        # prefill_decoder
        if cache_position.shape[1] > 1:
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

                outputs, _ = self.prefill_decoder(
                    sliced_input_ids.contiguous(),
                    attention_mask.contiguous(),
                    sliced_cache_positions.contiguous(),
                    torch.tensor(batch_idx, dtype=torch.int16),
                )
            outputs = outputs[:, query_length % self.prefill_chunk_size - 1].unsqueeze(1)
        # decoder
        else:
            attention_mask = self.decoder_attention_mask.clone()
            for b_idx in range(self.batch_size):
                attention_mask[b_idx, :, :, : cache_position[b_idx].item() + 1] = 1

            outputs = self.decoder(
                input_ids.contiguous(),
                attention_mask.contiguous(),
                cache_position.contiguous(),
                torch.tensor(0, dtype=torch.int16),
            )[0]

        return CausalLMOutputWithPast(
            logits=outputs,
        )
