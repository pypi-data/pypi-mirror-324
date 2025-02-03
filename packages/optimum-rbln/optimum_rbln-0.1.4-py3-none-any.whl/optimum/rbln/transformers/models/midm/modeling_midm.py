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
from transformers import AutoModelForCausalLM, PretrainedConfig, PreTrainedModel
from transformers.modeling_outputs import CausalLMOutputWithCrossAttentions

from ....modeling_base import RBLNBaseModel
from ....modeling_config import DEFAULT_COMPILED_MODEL_NAME, RBLNConfig, RBLNRuntimeConfig
from ....utils.runtime_utils import RBLNPytorchRuntime
from ....utils.save_utils import maybe_save_preprocessors
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


class RBLNMidmLMHeadModel(RBLNBaseModel, RBLNGenerationMixin):
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

        self.prefill_decoder = RBLNRuntimeDecoder(runtime=self.runtimes[0], main_input_name="input_ids")
        self.decoder = RBLNRuntimeDecoder(runtime=self.runtimes[1], main_input_name="input_ids")
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
    ) -> "RBLNMidmLMHeadModel":

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

        def update_configs(kwargs):
            max_seq_len = kwargs.get("rbln_max_seq_len", None)
            if max_seq_len is not None:
                kwargs.update({"max_position_embeddings": max_seq_len})

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

        kwargs = update_configs(kwargs)

        rbln_config_kwargs, rbln_constructor_kwargs = cls.pop_rbln_kwargs_from_kwargs(kwargs)

        model: MidmLMHeadModel = TasksManager.get_model_from_task(
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
            ignore_mismatched_sizes=True,
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

        def compile_midm():
            wrapped_decoder = MidmLMHeadModelWrapper(model).eval()
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
                (prefill_ir.outputs[1 + i], prefill_ir.inputs[3 + i]) for i in range(model.config.n_layer * 2)
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

        compile_midm()

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

    def _create_runtimes(self, rbln_device_map: Dict[str, int]) -> List[rebel.Runtime]:
        device_val = rbln_device_map[DEFAULT_COMPILED_MODEL_NAME]
        return [
            self.compiled_models[0].create_runtime(input_info_index=0, tensor_type="pt", device=device_val),
            self.compiled_models[0].create_runtime(input_info_index=1, tensor_type="pt", device=device_val),
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

    def __repr__(self):
        return repr(self.runtimes[0]) + "\n" + repr(self.runtimes[1])
