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

import inspect
import logging
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Tuple, Union

import rebel
import torch
from transformers import AutoConfig, AutoModelForCausalLM, PretrainedConfig, PreTrainedModel
from transformers.modeling_outputs import CausalLMOutputWithCrossAttentions

from ....modeling_base import RBLNModel
from ....modeling_config import DEFAULT_COMPILED_MODEL_NAME, RBLNConfig, RBLNRuntimeConfig
from ....utils.runtime_utils import RBLNPytorchRuntime
from ...generation.utils import RBLNGenerationMixin
from .hf_hub_cached.modeling_midm import MidmLMHeadModel
from .midm_architecture import (
    MidmLMHeadModelWrapper,
)


logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from transformers import (
        AutoFeatureExtractor,
        AutoProcessor,
        AutoTokenizer,
        PretrainedConfig,
    )


class RBLNRuntimeDecoder(RBLNPytorchRuntime):
    mandatory_members = ["main_input_name"]

    # RBLN_Runtimemodule
    def forward(
        self,
        input_ids: torch.LongTensor = None,
        attention_mask: torch.LongTensor = None,
        cache_position: torch.Tensor = None,
        **kwargs: Dict[str, Any],
    ):
        logits = super().forward(
            input_ids=input_ids,
            attention_mask=attention_mask,
            cache_position=cache_position,
        )
        return logits


class RBLNMidmLMHeadModel(RBLNModel, RBLNGenerationMixin):
    """
    The Midm Model transformer with a language modeling head on top (linear layer with weights tied to the input
    embeddings).

    This model inherits from [`RBLNBaseModel`]. Check the superclass documentation for the generic methods the
    library implements for all its model.

    It implements the methods to convert a pre-trained transformers Midm model into a RBLN transformer model by:
    - transferring the checkpoint weights of the original into an optimized RBLN graph,
    - compiling the resulting graph using the RBLN compiler.

    """

    model_type = "rbln_model"
    auto_model_class = AutoModelForCausalLM
    main_input_name = "input_ids"

    def __init__(
        self,
        models: List[Union[PreTrainedModel, rebel.RBLNCompiledModel]],
        config: PretrainedConfig = None,
        preprocessors: Optional[List] = None,
        rbln_config: Optional[RBLNConfig] = None,
        rbln_device: Optional[List[int]] = None,
        rbln_device_map: Optional[Dict[str, int]] = None,
        **kwargs,
    ):
        super().__init__(
            models,
            config,
            preprocessors,
            rbln_config,
            rbln_device=rbln_device,
            rbln_device_map=rbln_device_map,
            **kwargs,
        )
        self.batch_size = self.rbln_config.meta["rbln_batch_size"]
        self.prefill_chunk_size = self.rbln_config.meta["rbln_prefill_chunk_size"]
        self.max_seq_len = self.rbln_config.meta["rbln_max_seq_len"]

        self.prefill_attention_mask = torch.zeros(
            self.batch_size, 1, self.prefill_chunk_size, self.max_seq_len, dtype=torch.int64
        )
        self.causal_mask = 1 - torch.triu(
            torch.ones(self.batch_size, 1, self.prefill_chunk_size, self.prefill_chunk_size), diagonal=1
        )

        self.prefill_decoder = RBLNRuntimeDecoder(runtime=self.model[0], main_input_name="input_ids")
        self.decoder = RBLNRuntimeDecoder(runtime=self.model[1], main_input_name="input_ids")
        self.past_cached_length = 0

    def can_generate(self):
        return True

    def __getattr__(self, __name: str) -> Any:
        """This is the key method to implement RBLN-Midm.

        Returns:
            Any: Midm's corresponding method
        """

        def redirect(func):
            return lambda *pargs, **kwargs: func(self, *pargs, **kwargs)

        val = getattr(MidmLMHeadModel, __name)
        if isinstance(val, Callable) and "self" in set(inspect.signature(val).parameters):
            return redirect(val)
        return val

    def _reorder_cache(self, past_key_values, beam_idx):
        # TODO(jongho): implement
        raise NotImplementedError

    @classmethod
    @torch.inference_mode()
    def get_compiled_model(cls, model: "PreTrainedModel", rbln_config: RBLNConfig):
        wrapped_decoder = MidmLMHeadModelWrapper(model).eval()
        prefill_rbln_runtime_config = rbln_config[DEFAULT_COMPILED_MODEL_NAME][0]
        dec_rbln_runtime_config = rbln_config[DEFAULT_COMPILED_MODEL_NAME][1]

        prefill_example_inputs = prefill_rbln_runtime_config.get_dummy_inputs(fill=0)
        dec_example_inputs = dec_rbln_runtime_config.get_dummy_inputs(fill=0)

        prefill_scripted_model = torch.jit.trace(wrapped_decoder, prefill_example_inputs, check_trace=False)
        dec_scripted_model = torch.jit.trace(wrapped_decoder, dec_example_inputs, check_trace=False)

        prefill_ir = rebel.torchscript_to_ir(
            prefill_scripted_model,
            input_names=[v[0] for v in prefill_rbln_runtime_config.input_info],
        )
        dec_ir = rebel.torchscript_to_ir(
            dec_scripted_model,
            input_names=[v[0] for v in dec_rbln_runtime_config.input_info],
        )

        connections = [(prefill_ir.outputs[1 + i], prefill_ir.inputs[3 + i]) for i in range(model.config.n_layer * 2)]

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
            config = AutoConfig.from_pretrained(model_id, trust_remote_code=trust_remote_code)
            if hf_position_embedding := getattr(config, "max_position_embeddings", None):
                if hf_position_embedding < rbln_max_seq_len:
                    logger.warning(
                        f"`rbln_max_seq_len` is larger than original config({hf_position_embedding})."
                        "This may lead to incorrect inferences of the model."
                    )
            kwargs.update({"max_position_embeddings": rbln_max_seq_len})

        return super().get_pytorch_model(
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
            ignore_mismatched_sizes=True,
            **kwargs,
        )

    @classmethod
    def _get_rbln_config(
        cls,
        preprocessors: Union["AutoFeatureExtractor", "AutoProcessor", "AutoTokenizer"],
        model_config: "PretrainedConfig",
        rbln_prefill_chunk_size: Optional[int] = 128,
        rbln_max_seq_len: Optional[int] = None,
        rbln_batch_size: Optional[int] = None,
    ) -> RBLNConfig:
        meta = {}
        if rbln_max_seq_len is None:
            rbln_max_seq_len = getattr(model_config, "max_position_embeddings", None)

        if rbln_max_seq_len is None:
            for tokenizer in preprocessors:
                if hasattr(tokenizer, "model_max_length"):
                    rbln_max_seq_len = tokenizer.model_max_length
                    break
            if rbln_max_seq_len is None:
                raise ValueError("`rbln_max_seq_len` should be specified!")

        if rbln_batch_size is None:
            rbln_batch_size = 1

        meta["rbln_prefill_chunk_size"] = rbln_prefill_chunk_size
        meta["rbln_max_seq_len"] = rbln_max_seq_len
        meta["rbln_batch_size"] = rbln_batch_size if rbln_batch_size is not None else 1

        def get_input_info(query_length):
            input_info = [
                ("input_ids", [rbln_batch_size, query_length], "int64"),
                ("attention_mask", [rbln_batch_size, 1, query_length, rbln_max_seq_len], "int64"),
                (
                    "cache_position",
                    [],
                    "int32",
                ),
            ]
            input_info.extend(
                [
                    (
                        f"past_key_values_{i}",
                        [
                            rbln_batch_size,
                            model_config.n_head,
                            rbln_max_seq_len,
                            model_config.hidden_size // model_config.n_head,
                        ],
                        "float32",
                    )
                    for i in range(model_config.n_layer * 2)
                ]
            )
            return input_info

        # model input info
        prefill_input_info = get_input_info(query_length=rbln_prefill_chunk_size)
        dec_input_info = get_input_info(query_length=1)

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

    def prepare_inputs_for_generation(self, input_ids, past_key_values=0, attention_mask=None, **kwargs):
        batch_size, cur_len = input_ids.shape
        past_cached_length = past_key_values

        if past_cached_length == 0:
            mod_len = cur_len % self.prefill_chunk_size
            self.pad_len = self.prefill_chunk_size - mod_len if mod_len > 0 else 0

            prompt_attn_mask = torch.nn.functional.pad(attention_mask, (self.pad_len, 0), value=0)
            self.prompt_attn_mask = prompt_attn_mask.reshape(batch_size, 1, 1, -1).contiguous()

            input_ids = torch.nn.functional.pad(input_ids, (self.pad_len, 0), value=0)
            attention_mask = self.prefill_attention_mask.clone()
            cache_position = torch.tensor(past_cached_length, dtype=torch.int32)

            query_length = cur_len + self.pad_len
        else:
            attention_mask = torch.nn.functional.pad(
                attention_mask, (self.pad_len, self.max_seq_len - cur_len - self.pad_len)
            )
            attention_mask = attention_mask.reshape(batch_size, 1, 1, -1).contiguous()
            cache_position = torch.tensor(past_cached_length, dtype=torch.int32)
            input_ids = input_ids[:, -1:].contiguous()
            query_length = 1

        model_inputs = {
            "input_ids": input_ids,
            "past_key_values": past_cached_length,
            "attention_mask": attention_mask,
            "cache_position": cache_position,
            "query_length": query_length,
        }

        return model_inputs

    def forward(
        self,
        input_ids: Optional[torch.LongTensor] = None,
        past_key_values: int = None,
        attention_mask: Optional[torch.FloatTensor] = None,
        cache_position: Optional[torch.Tensor] = None,
        query_length: Optional[torch.Tensor] = None,
        **kwargs,
    ) -> Union[Tuple, CausalLMOutputWithCrossAttentions]:
        past_cached_length = past_key_values

        if past_cached_length is not None:
            past_cached_length += query_length

        if cache_position == 0:
            for step in range(0, query_length, self.prefill_chunk_size):
                sliced_input_ids = input_ids[:, step : step + self.prefill_chunk_size]
                attention_mask[:, :, :, :step] = 1
                attention_mask[:, :, :, step : step + self.prefill_chunk_size] = self.causal_mask
                attention_mask[:, :, :, :query_length] *= self.prompt_attn_mask

                output = self.prefill_decoder(
                    input_ids=sliced_input_ids.contiguous(),
                    attention_mask=attention_mask,
                    cache_position=cache_position + step,
                )
                cache_position += self.prefill_chunk_size
        else:
            output = self.decoder(
                input_ids=input_ids.contiguous(),
                attention_mask=attention_mask,
                cache_position=cache_position,
            )
        return CausalLMOutputWithCrossAttentions(logits=output, past_key_values=past_cached_length)
