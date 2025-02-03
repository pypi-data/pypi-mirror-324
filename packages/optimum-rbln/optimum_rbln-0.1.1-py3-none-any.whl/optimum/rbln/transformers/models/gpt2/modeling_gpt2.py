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
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Tuple, Union

import rebel
import torch
from optimum.exporters import TasksManager
from transformers import AutoModelForCausalLM, GPT2LMHeadModel, PretrainedConfig
from transformers.modeling_outputs import CausalLMOutputWithCrossAttentions, Seq2SeqLMOutput

from ....modeling_base import RBLNBaseModel
from ....modeling_config import DEFAULT_COMPILED_MODEL_NAME, RBLNConfig, RBLNRuntimeConfig
from ....utils.runtime_utils import RBLNPytorchRuntime
from ....utils.save_utils import maybe_save_preprocessors
from ...generation.utils import RBLNGenerationMixin
from .gpt2_architecture import GPT2LMHeadModelWrapper


logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from transformers import (
        AutoFeatureExtractor,
        AutoProcessor,
        AutoTokenizer,
        PretrainedConfig,
    )


class RBLNRuntimeDecoder(RBLNPytorchRuntime):
    def forward(self, *args, **kwargs) -> Union[Tuple, Seq2SeqLMOutput]:
        outputs = super().forward(*args, **kwargs)
        logits = outputs
        return Seq2SeqLMOutput(logits=logits)


class RBLNGPT2LMHeadModel(RBLNBaseModel, RBLNGenerationMixin):
    """
    The GPT2 Model transformer with a language modeling head on top (linear layer with weights tied to the input
    embeddings).

    This model inherits from [`RBLNBaseModel`]. Check the superclass documentation for the generic methods the
    library implements for all its model.

    It implements the methods to convert a pre-trained transformers GPT2 model into a RBLN transformer model by:
    - transferring the checkpoint weights of the original into an optimized RBLN graph,
    - compiling the resulting graph using the RBLN compiler.

    """

    model_type = "rbln_model"
    auto_model_class = AutoModelForCausalLM
    main_input_name = "input_ids"

    def __post_init__(self, **kwargs):
        self.prefill_chunk_size = self.rbln_config.meta["rbln_prefill_chunk_size"]
        self.max_seq_len = self.rbln_config.meta["rbln_max_seq_len"]

        batch_size = self.rbln_config[DEFAULT_COMPILED_MODEL_NAME][0].input_info[0][1][0]
        self.prefill_attention_mask = torch.zeros(
            batch_size, 1, self.prefill_chunk_size, self.max_seq_len, dtype=torch.int64
        )
        self.causal_mask = 1 - torch.triu(
            torch.ones(batch_size, 1, self.prefill_chunk_size, self.prefill_chunk_size), diagonal=1
        )

        self.prefill_decoder = RBLNRuntimeDecoder(runtime=self.runtimes[0])
        self.decoder = RBLNRuntimeDecoder(runtime=self.runtimes[1])
        self.pad_token_id = self.rbln_config.meta["rbln_pad_token_id"]
        self.past_cached_length = 0

    def can_generate(self):
        return True

    def __getattr__(self, __name: str) -> Any:
        """This is the key method to implement RBLN-GPT2.

        Returns:
            Any: GPT2's corresponding method
        """

        def redirect(func):
            return lambda *pargs, **kwargs: func(self, *pargs, **kwargs)

        val = getattr(GPT2LMHeadModel, __name)
        if isinstance(val, Callable) and "self" in set(inspect.signature(val).parameters):
            return redirect(val)
        return val

    def _reorder_cache(self, past_key_values, beam_idx):
        # TODO(jongho): implement
        raise NotImplementedError

    @classmethod
    def _export(
        cls,
        model_id: str,
        config: "PretrainedConfig",
        use_auth_token: Optional[Union[bool, str]] = None,
        revision: Optional[str] = None,
        force_download: bool = False,
        cache_dir: Optional[str] = None,
        subfolder: str = "",
        local_files_only: bool = False,
        trust_remote_code: bool = False,
        model_save_dir: Optional[Union[str, Path, TemporaryDirectory]] = None,
        **kwargs,
    ) -> "RBLNGPT2LMHeadModel":
        """
        Exports a vanilla Transformers model into a rbln-compiled Module.
        """
        task = kwargs.pop("task", None)
        if task is None:
            task = TasksManager.infer_task_from_model(cls.auto_model_class)

        if model_save_dir is None:
            save_dir = TemporaryDirectory()
            save_dir_path = Path(save_dir.name)
        else:
            save_dir = model_save_dir
            if isinstance(save_dir, TemporaryDirectory):
                save_dir_path = Path(model_save_dir.name)
            else:
                save_dir_path = Path(model_save_dir)
                save_dir_path.mkdir(exist_ok=True)

        kwargs.update(
            {
                "torchscript": True,
                "return_dict": False,
                "use_cache": True,
            }
        )

        rbln_config_kwargs, rbln_constructor_kwargs = cls.pop_rbln_kwargs_from_kwargs(kwargs)

        model: GPT2LMHeadModel = TasksManager.get_model_from_task(
            task=task,
            model_name_or_path=model_id,
            subfolder=subfolder,
            revision=revision,
            framework="pt",
            cache_dir=cache_dir,
            use_auth_token=use_auth_token,
            local_files_only=local_files_only,
            force_download=force_download,
            trust_remote_code=trust_remote_code,
            **kwargs,
        )

        if config is None:
            config = model.config

        config.save_pretrained(save_dir_path)
        preprocessors = maybe_save_preprocessors(model_id, save_dir_path, src_subfolder=subfolder)

        # Get compilation arguments
        if rbln_config_kwargs.get("rbln_config", None) is None:
            rbln_config = cls.get_rbln_config(
                preprocessors=preprocessors, model_config=model.config, **rbln_config_kwargs
            )

        def compile_gpt2():
            wrapped_decoder = GPT2LMHeadModelWrapper(model).eval()

            prefill_rbln_runtime_config = rbln_config[DEFAULT_COMPILED_MODEL_NAME][0]
            dec_rbln_runtime_config = rbln_config[DEFAULT_COMPILED_MODEL_NAME][1]

            prefill_example_inputs = prefill_rbln_runtime_config.get_dummy_inputs(fill=0)
            dec_example_inputs = dec_rbln_runtime_config.get_dummy_inputs(fill=0)

            prefill_scripted_model = torch.jit.trace(wrapped_decoder, prefill_example_inputs)
            dec_scripted_model = torch.jit.trace(wrapped_decoder, dec_example_inputs)

            prefill_ir = rebel.torchscript_to_ir(
                prefill_scripted_model,
                input_names=[v[0] for v in prefill_rbln_runtime_config.input_info],
            )
            dec_ir = rebel.torchscript_to_ir(
                dec_scripted_model,
                input_names=[v[0] for v in dec_rbln_runtime_config.input_info],
            )

            connections = [
                (prefill_ir.outputs[1], prefill_ir.inputs[1]),
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
            compiled_model.save(save_dir_path / f"{DEFAULT_COMPILED_MODEL_NAME}.rbln")

        compile_gpt2()
        rbln_config.save(save_dir_path)

        return cls._from_pretrained(
            model_id=save_dir_path,
            config=config,
            model_save_dir=save_dir,
            **rbln_constructor_kwargs,
            **kwargs,
        )

    @classmethod
    def _get_rbln_config(
        cls,
        preprocessors: Union["AutoFeatureExtractor", "AutoProcessor", "AutoTokenizer"],
        model_config: "PretrainedConfig",
        rbln_max_seq_len: Optional[int] = None,
        rbln_batch_size: Optional[int] = None,
        rbln_pad_token_id: Optional[int] = None,
    ) -> RBLNConfig:
        meta = {}

        default_max_length = getattr(model_config, "n_positions", None)
        for tokenizer in preprocessors:
            default_max_length = default_max_length or getattr(tokenizer, "max_len_single_sentence", None)

        prefill_chunk_size = 128

        if rbln_max_seq_len is None:
            rbln_max_seq_len = default_max_length

        if rbln_max_seq_len is None:
            raise ValueError("`rbln_max_seq_len` should be specified!")

        if rbln_pad_token_id is None:
            rbln_pad_token_id = getattr(model_config, "pad_token_id", None)
            if rbln_pad_token_id is None:
                rbln_pad_token_id = getattr(model_config, "eos_token_id", None)
                if rbln_pad_token_id is None:
                    rbln_pad_token_id = 50256

        meta["rbln_prefill_chunk_size"] = prefill_chunk_size
        meta["rbln_max_seq_len"] = rbln_max_seq_len
        meta["rbln_pad_token_id"] = rbln_pad_token_id

        rbln_batch_size = 1 if rbln_batch_size is None else rbln_batch_size

        def get_input_info(query_length):
            return [
                ("input_ids", [rbln_batch_size, query_length], "int64"),
                (
                    "past_key_values",
                    [
                        model_config.n_layer,
                        2,
                        rbln_batch_size,
                        model_config.n_head,
                        rbln_max_seq_len,
                        model_config.hidden_size // model_config.n_head,
                    ],
                    "float32",
                ),
                ("attention_mask", [rbln_batch_size, 1, query_length, rbln_max_seq_len], "int64"),
                (
                    "cache_position",
                    [],
                    "int32",
                ),
            ]

        # model input info
        prefill_input_info = get_input_info(query_length=prefill_chunk_size)
        dec_input_info = get_input_info(query_length=1)

        prefill_rbln_runtime_config = RBLNRuntimeConfig(input_info=prefill_input_info)
        dec_rbln_runtime_config = RBLNRuntimeConfig(input_info=dec_input_info)

        rbln_config = RBLNConfig.from_rbln_runtime_configs(
            [prefill_rbln_runtime_config, dec_rbln_runtime_config],
            _rbln_meta=meta,
        )

        return rbln_config

    def _create_runtimes(self, rbln_device_map: Dict[str, int]) -> List[rebel.Runtime]:
        device_val = rbln_device_map[DEFAULT_COMPILED_MODEL_NAME]
        return [
            self.compiled_models[0].create_runtime(input_info_index=0, tensor_type="pt", device=device_val),
            self.compiled_models[0].create_runtime(input_info_index=1, tensor_type="pt", device=device_val),
        ]

    def prepare_inputs_for_generation(self, input_ids, past_key_values=0, attention_mask=None, **kwargs):
        batch_size, cur_len = input_ids.shape
        past_cached_length = past_key_values

        # In greedy decoding
        if past_cached_length == 0:
            self.prompt_ids = input_ids
            self.rightpad_max_len = cur_len
            prompt_min_len = torch.min(torch.sum(attention_mask, dim=-1))
            self.dummy_len = torch.sum(attention_mask, dim=-1) - prompt_min_len

            if cur_len % self.prefill_chunk_size == 0:
                pad_len = 0
            else:
                pad_len = self.prefill_chunk_size - cur_len % self.prefill_chunk_size
            input_ids = torch.nn.functional.pad(input_ids, (0, pad_len))
            attention_mask = self.prefill_attention_mask.clone()
            cache_position = torch.tensor(past_cached_length, dtype=torch.int32)

            query_length = prompt_min_len.item()
        else:
            cache_position = torch.tensor(past_cached_length, dtype=torch.int32)
            attention_mask = torch.zeros(batch_size, 1, 1, self.max_seq_len, dtype=torch.int64)
            attention_mask[:, :, :, : cache_position + 1] = 1
            input_ids = input_ids[:, cache_position : cache_position + 1].contiguous()
            query_length = 1

        model_inputs = {
            "input_ids": input_ids,
            "past_key_values": past_key_values,
            "attention_mask": attention_mask,
            # below are rbln-related kwargs
            "cache_position": cache_position,
            "query_length": query_length,
        }

        return model_inputs

    def forward(
        self,
        input_ids: Optional[torch.LongTensor] = None,
        past_key_values: Optional[Tuple[Tuple[torch.Tensor]]] = None,
        attention_mask: Optional[torch.FloatTensor] = None,
        cache_position: Optional[torch.Tensor] = None,
        query_length: Optional[torch.Tensor] = None,
        **kwargs,
    ) -> Union[Tuple, CausalLMOutputWithCrossAttentions]:
        if past_key_values is not None:
            past_key_values += query_length

        if cache_position == 0:
            for step in range(0, query_length, self.prefill_chunk_size):
                sliced_input_ids = input_ids[:, step : step + self.prefill_chunk_size]
                attention_mask[:, :, :, :step] = 1
                attention_mask[:, :, :, step : step + self.prefill_chunk_size] = self.causal_mask

                output = self.prefill_decoder(
                    input_ids=sliced_input_ids.contiguous(),
                    attention_mask=attention_mask.contiguous(),
                    cache_position=cache_position + step,
                )

            idx = query_length % self.prefill_chunk_size - 1
            output = output.logits[:, idx].unsqueeze(1)

        else:
            output = self.decoder(
                input_ids=input_ids.contiguous(),
                attention_mask=attention_mask.contiguous(),
                cache_position=cache_position,
            )
            output = output.logits

        return CausalLMOutputWithCrossAttentions(logits=output, past_key_values=past_key_values)

    def __repr__(self):
        return repr(self.runtimes[0]) + "\n" + repr(self.runtimes[1])
