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
import functools
import glob
import os
from abc import ABC
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

import rebel  # noqa: F401
import torch  # noqa: F401
from safetensors.torch import load_file
from transformers import AutoConfig, AutoModelForCausalLM, PretrainedConfig, PreTrainedModel
from transformers.modeling_utils import no_init_weights
from transformers.utils import ModelOutput

from ....modeling_base import RBLNModel
from ....modeling_config import DEFAULT_COMPILED_MODEL_NAME, RBLNCompileConfig, RBLNConfig
from ....utils.logging import get_logger
from ....utils.runtime_utils import RBLNPytorchRuntime
from ....utils.timer_utils import rbln_timer


logger = get_logger()

if TYPE_CHECKING:
    from transformers import (
        AutoFeatureExtractor,
        AutoProcessor,
        AutoTokenizer,
        PretrainedConfig,
    )

SUPPORTED_QUANTIZATIONS = {
    "rbln": [
        "w4a16",
    ],
}


class RBLNRuntimeModel(RBLNPytorchRuntime):
    mandatory_members = ["main_input_name", "embed_tokens"]

    def forward(
        self,
        input_ids: torch.LongTensor,
        inputs_embeds: torch.Tensor,
        attention_mask: torch.Tensor,
        cache_position: torch.Tensor,
        batch_position: torch.Tensor,
        query_idx: torch.Tensor,
        **kwargs,
    ):
        if inputs_embeds is None:
            inp = input_ids
            if self.embed_tokens is not None:
                inp = self.embed_tokens(inp)

            return super().forward(
                inp,
                attention_mask,
                cache_position,
                batch_position,
                query_idx,
                **kwargs,
            )
        else:
            return super().forward(
                inputs_embeds,
                attention_mask,
                cache_position,
                batch_position,
                query_idx,
                **kwargs,
            )


@dataclass
class RBLNDecoderOnlyOutput(ModelOutput):
    logits: torch.FloatTensor = None
    generate_idx: torch.Tensor = None


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
        self.batch_size = self.rbln_config.model_cfg["batch_size"]
        self.max_seq_len = self.rbln_config.model_cfg["max_seq_len"]
        self.prefill_chunk_size = self.rbln_config.model_cfg["prefill_chunk_size"]

        self.prefill_attention_mask = torch.zeros(1, 1, self.prefill_chunk_size, self.max_seq_len, dtype=torch.float32)
        self.causal_mask = 1 - torch.triu(
            torch.ones(1, 1, self.prefill_chunk_size, self.prefill_chunk_size), diagonal=1
        )
        self.dec_attn_mask_init = torch.zeros(1, 1, 1, self.max_seq_len, dtype=torch.float32)
        self.dec_attn_mask = torch.zeros(self.batch_size, 1, 1, self.max_seq_len, dtype=torch.float32)

        main_input_name = self.main_input_name
        if self.rbln_config.model_cfg["use_inputs_embeds"]:
            main_input_name = "inputs_embeds"
            artifacts = torch.load(self.model_save_dir / self.subfolder / "torch_artifacts.pth", weights_only=False)
            with no_init_weights():
                self.embed_tokens = torch.nn.Embedding(
                    self.config.vocab_size,
                    self.config.hidden_size,
                    self.config.pad_token_id,
                )
            self.embed_tokens.load_state_dict(artifacts["embed_tokens"])
        else:
            self.embed_tokens = None

        self.prefill_decoder = RBLNRuntimeModel(
            runtime=self.model[0], main_input_name=main_input_name, embed_tokens=self.embed_tokens
        )
        self.decoder = RBLNRuntimeModel(
            runtime=self.model[1], main_input_name=main_input_name, embed_tokens=self.embed_tokens
        )

    @classmethod
    def save_torch_artifacts(
        cls,
        model: "PreTrainedModel",
        save_dir_path: Path,
        subfolder: str,
        rbln_config: RBLNConfig,
    ):
        """
        If you are unavoidably running on a CPU rather than an RBLN device,
        store the torch tensor, weight, etc. in this function.
        """
        if rbln_config.model_cfg["use_inputs_embeds"]:
            save_dict = {}
            save_dict["embed_tokens"] = model.get_input_embeddings().state_dict()
            torch.save(save_dict, save_dir_path / subfolder / "torch_artifacts.pth")

    def get_input_embeddings(self):
        return self.embed_tokens

    @classmethod
    def get_quantized_model(
        cls,
        model_id: str,
        use_auth_token: Optional[Union[bool, str]] = None,
        revision: Optional[str] = None,
        force_download: bool = False,
        cache_dir: Optional[str] = None,
        subfolder: str = "",
        local_files_only: bool = False,
        trust_remote_code: bool = False,
        **kwargs,
    ):
        from ...utils.rbln_quantization import update_layers_to_quantized

        kwargs = cls.update_kwargs(kwargs)

        config = AutoConfig.from_pretrained(
            model_id,
            use_auth_token=use_auth_token,
            revision=revision,
            force_download=force_download,
            cache_dir=cache_dir,
            trust_remote_code=trust_remote_code,
            **kwargs,
        )

        with no_init_weights():
            model = AutoModelForCausalLM.from_config(config)

        update_layers_to_quantized(model)

        n_layer = kwargs.get("num_hidden_layers", None)
        cls._load_weights_directly_to_model(model, model_id, n_layer)

        return model

    def _load_weights_directly_to_model(model, model_id, n_layer=None):
        """
        Load safetensor file data directly into the model, filtering by layer if n_layer is provided.
        """

        model_params = dict(model.named_parameters(recurse=True))
        model_buffers = dict(model.named_buffers(recurse=True))
        safetensor_files = glob.glob(f"{model_id}/*.safetensors")

        target_layers = list(range(n_layer)) if n_layer is not None else None

        for safetensor_file in safetensor_files:
            file_data = load_file(safetensor_file)
            for key, value in file_data.items():
                if target_layers is not None:
                    parts = key.split(".")

                    if len(parts) > 2 and parts[2].isdigit() and (int(parts[2]) not in target_layers):
                        continue

                if key in model_params:
                    model_params[key].data.copy_(value)
                elif key in model_buffers:
                    model_buffers[key].data.copy_(value)

        return 0

    @classmethod
    def get_pytorch_model(cls, *args, **kwargs) -> "PreTrainedModel":
        rbln_kwargs = kwargs.get("rbln_kwargs", {})
        rbln_quantization = rbln_kwargs.get("quantization", None)

        if rbln_quantization is not None and rbln_quantization["format"] == "rbln":
            model = cls.get_quantized_model(*args, **kwargs)
        else:
            model = super().get_pytorch_model(*args, **kwargs)

        return model

    def validate_quantization_config(quantize_config):
        if quantize_config is not None:
            q_format = quantize_config.get("format")
            q_precision = quantize_config.get("precision")

            if q_format not in SUPPORTED_QUANTIZATIONS:
                raise ValueError(
                    f"Invalid quantization format: {q_format}. "
                    f"Supported formats are: {list(SUPPORTED_QUANTIZATIONS.keys())}"
                )

            if q_precision not in SUPPORTED_QUANTIZATIONS[q_format]:
                raise ValueError(
                    f"Invalid precision: {q_precision} for format: {q_format}. "
                    f"Supported precisions are: {SUPPORTED_QUANTIZATIONS[q_format]}"
                )

        return quantize_config

    @classmethod
    def set_quantize_env(cls, quantize_config):
        RBLN_QUANT_BITS_ENV = "RBLN_QUANT_BITS"
        quantize_config = cls.validate_quantization_config(quantize_config)
        if quantize_config is not None:
            q_precision = quantize_config.get("precision")
            quant_bits = q_precision.split("w")[1].split("a")[0]
            os.environ[RBLN_QUANT_BITS_ENV] = quant_bits
            return RBLN_QUANT_BITS_ENV
        return None

    @classmethod
    def reset_quantize_env(cls, env_var_name):
        if env_var_name is not None and env_var_name in os.environ:
            del os.environ[env_var_name]

    @classmethod
    def manage_quantize_env(cls, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            quantize_config = kwargs.get("quantize_config")
            quantize_env_var = cls.set_quantize_env(quantize_config)
            try:
                return func(*args, **kwargs)
            finally:
                cls.reset_quantize_env(quantize_env_var)

        return wrapper

    @classmethod
    @torch.inference_mode()
    def get_compiled_model(cls, model: "PreTrainedModel", rbln_config: RBLNConfig):
        wrapped_model = cls.wrap_model_if_needed(model, rbln_config)

        rbln_compile_configs = rbln_config.compile_cfgs
        prefill_rbln_compile_config = rbln_compile_configs[0]
        dec_rbln_compile_config = rbln_compile_configs[1]

        @rbln_timer("JIT trace")
        def get_scripted_model():
            # This function is nested to dealloc the example inputs before compilation.
            prefill_example_inputs = prefill_rbln_compile_config.get_dummy_inputs(fill=0)
            dec_example_inputs = dec_rbln_compile_config.get_dummy_inputs(fill=4)

            batch_index = 3
            dec_example_inputs[batch_index].fill_(-1)  # fill batch_position -1 to indicate it is decoder.

            prefill_scripted_model = torch.jit.trace(
                wrapped_model, prefill_example_inputs, check_trace=False, _store_inputs=False
            )
            dec_scripted_model = torch.jit.trace(
                wrapped_model, dec_example_inputs, check_trace=False, _store_inputs=False
            )
            return prefill_scripted_model, dec_scripted_model

        prefill_scripted_model, dec_scripted_model = get_scripted_model()

        @rbln_timer("Model conversion")
        def scripted_model_to_ir():
            prefill_ir = rebel.torchscript_to_ir(
                prefill_scripted_model,
                input_names=[v[0] for v in prefill_rbln_compile_config.input_info],
            )
            dec_ir = rebel.torchscript_to_ir(
                dec_scripted_model,
                input_names=[v[0] for v in dec_rbln_compile_config.input_info],
            )
            return prefill_ir, dec_ir

        prefill_ir, dec_ir = scripted_model_to_ir()
        # Caching prefill_decoder/decoder I/O
        cache_index_offset = 5
        connections = [
            (prefill_ir.outputs[1 + i], prefill_ir.inputs[cache_index_offset + i])
            for i in range(model.config.num_hidden_layers * 2)
        ]

        # Extract quantize_config from rbln_config
        quantize_config = rbln_config.model_cfg.get("quantization", None)

        @cls.manage_quantize_env
        def compile_model(*args, **kwargs):
            # Remove quantize_config from kwargs
            kwargs.pop("quantize_config", None)

            # Call rebel.compile with the updated kwargs
            return rebel.compile(*args, **kwargs)

        compiled_model = compile_model(
            prefill_ir,
            dec_ir,
            connections=connections,
            fusion=prefill_rbln_compile_config.fusion,
            npu=prefill_rbln_compile_config.npu,
            tensor_parallel_size=prefill_rbln_compile_config.tensor_parallel_size,
            use_weight_sharing=True,
            quantize_config=quantize_config,
        )

        return compiled_model

    @classmethod
    def _get_rbln_config(
        cls,
        preprocessors: Union["AutoFeatureExtractor", "AutoProcessor", "AutoTokenizer"],
        model_config: "PretrainedConfig",
        rbln_kwargs: Dict[str, Any] = {},
    ) -> RBLNConfig:
        rbln_max_seq_len = rbln_kwargs.get("max_seq_len", None)
        rbln_batch_size = rbln_kwargs.get("batch_size", None)
        rbln_quantization = rbln_kwargs.get("quantization", None)
        rbln_use_inputs_embeds = rbln_kwargs.get("use_inputs_embeds", None)

        rbln_quantization = cls.validate_quantization_config(rbln_quantization)

        prefill_chunk_size = 128
        if rbln_max_seq_len is None:
            rbln_max_seq_len = getattr(model_config, "max_position_embeddings", None) or getattr(
                model_config, "n_positions", None
            )
        if rbln_max_seq_len is None:
            raise ValueError("`rbln_max_seq_len` should be specified.")
        rbln_batch_size = 1 if rbln_batch_size is None else rbln_batch_size
        rbln_use_inputs_embeds = False if rbln_use_inputs_embeds is None else rbln_use_inputs_embeds

        num_attention_heads = getattr(model_config, "n_head", None) or getattr(model_config, "num_attention_heads")
        num_key_value_heads = getattr(model_config, "num_key_value_heads", None) or num_attention_heads
        num_hidden_layers = getattr(model_config, "n_layer", None) or getattr(model_config, "num_hidden_layers")
        head_dim = getattr(model_config, "head_dim", None) or model_config.hidden_size // num_attention_heads
        hidden_size = getattr(model_config, "n_embd", None) or getattr(model_config, "hidden_size")

        def get_input_info(
            batch_size,
            query_length,
            use_inputs_embeds,
            hidden_size,
        ):
            if use_inputs_embeds:
                main_input = ("inputs_embeds", [batch_size, query_length, hidden_size], "float32")
            else:
                main_input = ("input_ids", [batch_size, query_length], "int64")

            input_info = [
                main_input,
                ("attention_mask", [batch_size, 1, query_length, rbln_max_seq_len], "float32"),
                (
                    "cache_position",
                    [batch_size, query_length],
                    "int32",
                ),
                ("batch_position", [], "int16"),
                ("query_idx", [], "int16"),
            ]

            input_info.extend(
                [
                    (
                        f"past_key_values_{i}",
                        [
                            rbln_batch_size,
                            num_key_value_heads,
                            rbln_max_seq_len,
                            head_dim,
                        ],
                        "float32",
                    )
                    for i in range(num_hidden_layers * 2)
                ]
            )

            return input_info

        prefill_input_info = get_input_info(
            batch_size=1,
            query_length=prefill_chunk_size,
            use_inputs_embeds=rbln_use_inputs_embeds,
            hidden_size=hidden_size,
        )
        dec_input_info = get_input_info(
            batch_size=rbln_batch_size,
            query_length=1,
            use_inputs_embeds=rbln_use_inputs_embeds,
            hidden_size=hidden_size,
        )

        prefill_rbln_compile_config = RBLNCompileConfig(input_info=prefill_input_info)
        dec_rbln_compile_config = RBLNCompileConfig(input_info=dec_input_info)

        rbln_config = RBLNConfig(
            rbln_cls=cls.__name__,
            compile_cfgs=[prefill_rbln_compile_config, dec_rbln_compile_config],
            rbln_kwargs=rbln_kwargs,
        )

        rbln_config.model_cfg.update(
            {
                "max_seq_len": rbln_max_seq_len,
                "batch_size": rbln_batch_size,
                "prefill_chunk_size": prefill_chunk_size,
                "use_inputs_embeds": rbln_use_inputs_embeds,
            }
        )

        if rbln_quantization is not None:
            rbln_config.model_cfg.update({"quantization": rbln_quantization})

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

    def prepare_inputs_for_generation(
        self,
        input_ids: torch.LongTensor,
        generate_idx: Optional[torch.Tensor] = None,
        attention_mask: Optional[torch.LongTensor] = None,
        inputs_embeds: Optional[torch.Tensor] = None,
        **kwargs,
    ):
        model_inputs = {}
        is_prefill_phase = generate_idx is None

        if is_prefill_phase:
            generate_idx = attention_mask.sum(dim=-1, keepdim=True).int()
            cache_position = None
        else:
            if inputs_embeds is not None:
                raise NotImplementedError("Specifying inputs_embeds in decoder phase is not supported.")

            input_ids = input_ids[:, -1:]
            cache_position = generate_idx
            generate_idx = generate_idx + 1
            model_inputs.update({"input_ids": input_ids})

        if inputs_embeds is not None:
            if self.rbln_config.model_cfg["use_inputs_embeds"]:
                model_inputs.update({"inputs_embeds": inputs_embeds})
            else:
                raise ValueError(
                    "The specifying inputs_embedst is only supported when using a compiled RBLN model with 'rbln_use_inputs_embeds' set to True."
                )
        else:
            model_inputs.update({"input_ids": input_ids})

        model_inputs.update(
            {
                "attention_mask": attention_mask,
                "cache_position": cache_position,
                "generate_idx": generate_idx,
            }
        )

        return model_inputs

    def _update_model_kwargs_for_generation(
        self,
        outputs: RBLNDecoderOnlyOutput,
        model_kwargs: Dict[str, Any],
        **kwargs,
    ) -> Dict[str, Any]:
        # update generate_idx
        model_kwargs["generate_idx"] = outputs.generate_idx

        return model_kwargs

    def forward(
        self,
        input_ids: Optional[torch.LongTensor] = None,
        inputs_embeds: Optional[torch.Tensor] = None,
        cache_position: Optional[torch.Tensor] = None,
        attention_mask: Optional[torch.LongTensor] = None,
        generate_idx: Optional[torch.Tensor] = None,
        # from llava_next forward args
        batch_idx: Optional[int] = None,
        **kwargs,
    ) -> Tuple[torch.FloatTensor]:
        # prefll
        if cache_position is None:
            logits = []
            input_tensors = inputs_embeds if inputs_embeds is not None else input_ids
            batch_size = input_tensors.shape[0]

            for b_idx in range(batch_size):
                # Transform inputs as vllm format
                if attention_mask is not None:
                    input_tensor = input_tensors[b_idx : b_idx + 1, attention_mask[b_idx].bool()]
                else:
                    input_tensor = input_tensors[b_idx : b_idx + 1]

                cache_position = torch.arange(0, generate_idx[b_idx].item(), dtype=torch.int32).unsqueeze(0)

                logit = self._forward_prefill(
                    input_ids=input_tensor if inputs_embeds is None else None,
                    inputs_embeds=input_tensor if inputs_embeds is not None else None,
                    cache_position=cache_position,
                    batch_idx=b_idx if batch_idx is None else batch_idx,  # Llava-next prefill
                )
                logits.append(logit)
            logits = torch.cat(logits, dim=0)
        # decoder
        else:
            logits = self._forward_decoder(
                input_ids=input_ids,
                inputs_embeds=inputs_embeds,
                cache_position=cache_position,
            )

        return RBLNDecoderOnlyOutput(
            logits=logits,
            generate_idx=generate_idx,
        )

    def _forward_prefill(
        self,
        input_ids: torch.LongTensor = None,
        inputs_embeds: torch.Tensor = None,
        cache_position: torch.Tensor = None,
        batch_idx: int = None,
    ) -> torch.FloatTensor:
        if batch_idx is None or batch_idx >= self.batch_size:
            raise RuntimeError(
                f"Invalid batch_idx ({batch_idx}). It must be a non-null value less than the batch size ({self.batch_size})."
            )

        out_buffers = [
            torch.empty(
                size=[
                    1,
                    1,
                    self.config.vocab_size,
                ],
                dtype=torch.float32,
                device="cpu",
            ),
            torch.empty(size=[], dtype=torch.int16, device="cpu"),
        ]

        input_tensors = inputs_embeds if inputs_embeds is not None else input_ids
        query_length = input_tensors.shape[1]
        _attention_mask = self.prefill_attention_mask.clone()

        for step in range(0, query_length, self.prefill_chunk_size):
            # pad input_tensors & cache_position for prefill_chunk
            if (step + self.prefill_chunk_size) > query_length:
                pad_to_chunk = step + self.prefill_chunk_size - query_length
                if inputs_embeds is not None:
                    input_tensors = torch.nn.functional.pad(input_tensors, (0, 0, 0, pad_to_chunk))
                else:
                    input_tensors = torch.nn.functional.pad(input_tensors, (0, pad_to_chunk))

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

            # slice input_tensor & cache_position with prefill_chunk_size
            _input_tensors = input_tensors[:, step : step + self.prefill_chunk_size]
            _cache_position = cache_position[:, step : step + self.prefill_chunk_size]

            # update attention_mask
            if step >= self.prefill_chunk_size:
                _attention_mask[:, :, :, step - self.prefill_chunk_size : step] = 1
            _attention_mask[:, :, :, step : step + self.prefill_chunk_size] = self.causal_mask

            query_idx = (query_length - 1) % self.prefill_chunk_size

            logits, _ = self.prefill_decoder(
                input_ids=_input_tensors.contiguous() if inputs_embeds is None else None,
                inputs_embeds=_input_tensors.contiguous() if inputs_embeds is not None else None,
                attention_mask=_attention_mask.contiguous(),
                cache_position=_cache_position.contiguous(),
                batch_position=torch.tensor(batch_idx, dtype=torch.int16),
                query_idx=torch.tensor(query_idx, dtype=torch.int16),
                out=out_buffers,
            )

        # update decoder_attn_mask with preprocessed kv-cache length in prefill phase
        self.dec_attn_mask[batch_idx] = self.dec_attn_mask_init.clone()
        self.dec_attn_mask[batch_idx, :, :, :query_length] = 1

        return logits

    def _forward_decoder(
        self,
        input_ids: torch.LongTensor = None,
        inputs_embeds: torch.Tensor = None,
        cache_position: torch.Tensor = None,
    ) -> torch.FloatTensor:
        input_tensors = inputs_embeds if inputs_embeds is not None else input_ids

        batch_size = input_tensors.shape[0]

        for b_idx in range(batch_size):
            decoding_step = cache_position[b_idx].item()
            self.dec_attn_mask[b_idx, :, :, decoding_step] = 1

        logits, _ = self.decoder(
            input_ids=input_tensors.contiguous() if inputs_embeds is None else None,
            inputs_embeds=input_tensors.contiguous() if inputs_embeds is not None else None,
            attention_mask=self.dec_attn_mask.contiguous(),
            cache_position=cache_position.contiguous(),
            batch_position=torch.tensor(0, dtype=torch.int16),
            query_idx=torch.tensor(0, dtype=torch.int16),
        )

        return logits

    def vllm_forward(
        self,
        input_ids: torch.LongTensor = None,
        inputs_embeds: torch.Tensor = None,
        cache_position: torch.Tensor = None,
        batch_idx: Optional[int] = None,
        **kwargs,
    ) -> Tuple[torch.FloatTensor]:
        # prefll
        if cache_position.shape[-1] > 1:
            logits = self._forward_prefill(
                input_ids=input_ids,
                inputs_embeds=inputs_embeds,
                cache_position=cache_position,
                batch_idx=batch_idx,
            )
        # decoder
        else:
            logits = self._forward_decoder(
                input_ids=input_ids,
                inputs_embeds=inputs_embeds,
                cache_position=cache_position,
            )

        return RBLNDecoderOnlyOutput(
            logits=logits,
        )
