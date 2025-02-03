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
from abc import ABC
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

import rebel  # noqa: F401
import torch  # noqa: F401
from transformers import AutoModelForSeq2SeqLM, GenerationConfig, PretrainedConfig, PreTrainedModel
from transformers.modeling_outputs import BaseModelOutput, Seq2SeqLMOutput

from ....modeling_base import RBLNModel
from ....modeling_config import DEFAULT_COMPILED_MODEL_NAME, RBLNCompileConfig, RBLNConfig
from ....utils.runtime_utils import RBLNPytorchRuntime


logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from transformers import (
        AutoFeatureExtractor,
        AutoProcessor,
        AutoTokenizer,
        PretrainedConfig,
    )


class RBLNRuntimeEncoder(RBLNPytorchRuntime):
    mandatory_members = ["main_input_name"]

    def forward(self, *args: List[torch.Tensor], **kwargs: Dict[str, torch.Tensor]):
        _ = super().forward(*args, **kwargs)
        return BaseModelOutput(last_hidden_state=torch.tensor([1.0]))


class RBLNRuntimeDecoder(RBLNPytorchRuntime):
    mandatory_members = ["main_input_name"]

    def forward(self, *args: List[torch.Tensor], **kwargs: Dict[str, torch.Tensor]):
        outputs = super().forward(*args, **kwargs)
        return Seq2SeqLMOutput(logits=outputs)


class RBLNModelForSeq2SeqLM(RBLNModel, ABC):
    """
    This is a generic model class that will be instantiated as one of the model classes of the library (with a sequence-to-sequence language modeling head) when created with the from_pretrained() class method.
    This model inherits from [`RBLNBaseModel`]. Check the superclass documentation for the generic methods the library implements for all its models.

    A class to convert and run pre-trained transformers based Seq2SeqLM models on RBLN devices.
    It implements the methods to convert a pre-trained transformers Seq2SeqLM model into a RBLN transformer model by:
    - transferring the checkpoint weights of the original into an optimized RBLN graph,
    - compiling the resulting graph using the RBLN compiler.

    Currently, this model class only supports the 'bart' and 't5' models from the transformers library. Future updates may include support for additional model types.
    """

    main_input_name = "input_ids"
    auto_model_class = AutoModelForSeq2SeqLM

    def __post_init__(self, **kwargs):
        self.encoder = RBLNRuntimeEncoder(runtime=self.model[0], main_input_name="input_ids")
        self.decoder = RBLNRuntimeDecoder(runtime=self.model[1], main_input_name="input_ids")

    @classmethod
    @torch.inference_mode()
    def get_compiled_model(cls, model: PreTrainedModel, rbln_config: RBLNConfig):
        wrapped_model = cls.wrap_model_if_needed(model, rbln_config)

        wrapped_model.encoder.encoder_max_length = rbln_config.model_cfg["enc_max_seq_len"]
        wrapped_model.encoder.decoder_max_length = rbln_config.model_cfg["dec_max_seq_len"]

        wrapped_model.decoder.encoder_max_length = rbln_config.model_cfg["enc_max_seq_len"]
        wrapped_model.decoder.decoder_max_length = rbln_config.model_cfg["dec_max_seq_len"]

        enc_rbln_compile_config = rbln_config.compile_cfgs[0]
        dec_rbln_compile_config = rbln_config.compile_cfgs[1]

        enc_example_inputs = enc_rbln_compile_config.get_dummy_inputs(fill=0)
        dec_example_inputs = dec_rbln_compile_config.get_dummy_inputs(fill=0)

        enc_example_inputs[3].fill_(0)
        dec_example_inputs[4].fill_(-1)

        enc_scripted_model = torch.jit.trace(wrapped_model.encoder, enc_example_inputs, check_trace=False)
        dec_scripted_model = torch.jit.trace(wrapped_model.decoder, dec_example_inputs, check_trace=False)

        enc_ir = rebel.torchscript_to_ir(
            enc_scripted_model,
            input_names=[v[0] for v in enc_rbln_compile_config.input_info],
            name=enc_rbln_compile_config.mod_name,
        )
        dec_ir = rebel.torchscript_to_ir(
            dec_scripted_model,
            input_names=[v[0] for v in dec_rbln_compile_config.input_info],
            name=dec_rbln_compile_config.mod_name,
        )

        connections = [
            (enc_ir.outputs[0], enc_ir.inputs[2], dec_ir.inputs[6]),
            (dec_ir.outputs[1], dec_ir.inputs[5]),
        ]

        compiled_model = rebel.compile(
            enc_ir,
            dec_ir,
            connections=connections,
            fusion=enc_rbln_compile_config.fusion,
            npu=enc_rbln_compile_config.npu,
            tensor_parallel_size=enc_rbln_compile_config.tensor_parallel_size,
        )
        return compiled_model

    @classmethod
    def _get_rbln_config(
        cls,
        preprocessors: Union["AutoFeatureExtractor", "AutoProcessor", "AutoTokenizer"],
        model_config: "PretrainedConfig",
        rbln_kwargs: Dict[str, Any] = {},
    ) -> RBLNConfig:
        rbln_enc_max_seq_len = rbln_kwargs.get("enc_max_seq_len", None)
        rbln_dec_max_seq_len = rbln_kwargs.get("dec_max_seq_len", None)
        rbln_batch_size = rbln_kwargs.get("batch_size", None)
        rbln_batch_size = 1 if rbln_batch_size is None else rbln_batch_size

        n_layer = getattr(model_config, "decoder_layers", None) or getattr(model_config, "num_layers")
        n_head = getattr(model_config, "decoder_attention_heads", None) or getattr(model_config, "num_heads")
        d_kv = (
            model_config.d_kv
            if hasattr(model_config, "d_kv")
            else model_config.d_model // model_config.encoder_attention_heads
        )

        max_position_embeddings = getattr(model_config, "n_positions", None) or getattr(
            model_config, "max_position_embeddings", None
        )

        rbln_pad_token_id = getattr(model_config, "pad_token_id", None)
        if rbln_pad_token_id is None:
            rbln_pad_token_id = getattr(model_config, "bos_token_id", None)
            if rbln_pad_token_id is None:
                rbln_pad_token_id = getattr(model_config, "eos_token_id", None)
                if rbln_pad_token_id is None:
                    rbln_pad_token_id = -1

        if rbln_enc_max_seq_len is None:
            rbln_enc_max_seq_len = max_position_embeddings
            if rbln_enc_max_seq_len is None:
                for tokenizer in preprocessors:
                    if hasattr(tokenizer, "model_max_length"):
                        rbln_enc_max_seq_len = tokenizer.model_max_length
                        break
                if rbln_enc_max_seq_len is None:
                    raise ValueError("`rbln_enc_max_seq_len` should be specified!")
        if max_position_embeddings is not None and rbln_enc_max_seq_len > max_position_embeddings:
            raise ValueError("`rbln_enc_max_seq_len` should be less or equal than max_position_embeddings!")

        if rbln_dec_max_seq_len is None:
            rbln_dec_max_seq_len = max_position_embeddings
            if rbln_dec_max_seq_len is None:
                for tokenizer in preprocessors:
                    if hasattr(tokenizer, "model_max_length"):
                        rbln_dec_max_seq_len = tokenizer.model_max_length
                        break
                if rbln_dec_max_seq_len is None:
                    raise ValueError("`rbln_dec_max_seq_len` should be specified!")

        if max_position_embeddings is not None and rbln_dec_max_seq_len > max_position_embeddings:
            raise ValueError("`rbln_dec_max_seq_len` should be less or equal than max_position_embeddings!")

        # model input info
        enc_input_info = [
            ("input_ids", [1, rbln_enc_max_seq_len], "int64"),
            ("attention_mask", [1, rbln_enc_max_seq_len], "float32"),
            (
                "cross_key_value_states",
                [
                    n_layer * 2,
                    rbln_batch_size,
                    n_head,
                    rbln_enc_max_seq_len,
                    d_kv,
                ],
                "float32",
            ),
            ("batch_idx", [], "int32"),
        ]

        dec_input_info = [
            ("input_ids", [rbln_batch_size, 1], "int64"),
            ("attention_mask", [rbln_batch_size, rbln_dec_max_seq_len], "float32"),
            ("encoder_attention_mask", [rbln_batch_size, rbln_enc_max_seq_len], "float32"),
            (
                "cache_position",
                [rbln_batch_size, 1],
                "int32",
            ),
            ("batch_position", [], "int32"),
        ]
        dec_input_info.extend(
            [
                (
                    "self_key_value_states",
                    [
                        n_layer * 2,
                        rbln_batch_size,
                        n_head,
                        rbln_dec_max_seq_len,
                        d_kv,
                    ],
                    "float32",
                )
            ]
        )
        dec_input_info.extend(
            [
                (
                    "cross_key_value_states",
                    [
                        n_layer * 2,
                        rbln_batch_size,
                        n_head,
                        rbln_enc_max_seq_len,
                        d_kv,
                    ],
                    "float32",
                )
            ]
        )
        enc_rbln_compile_config = RBLNCompileConfig(mod_name="encoder", input_info=enc_input_info)
        dec_rbln_compile_config = RBLNCompileConfig(mod_name="decoder", input_info=dec_input_info)

        rbln_config = RBLNConfig(
            rbln_cls=cls.__name__,
            compile_cfgs=[enc_rbln_compile_config, dec_rbln_compile_config],
            rbln_kwargs=rbln_kwargs,
        )

        rbln_config.model_cfg.update(
            {
                "enc_max_seq_len": rbln_enc_max_seq_len,
                "dec_max_seq_len": rbln_dec_max_seq_len,
                "batch_size": rbln_batch_size,
                "pad_token_id": rbln_pad_token_id,
            }
        )

        return rbln_config

    @classmethod
    def _create_runtimes(
        cls, compiled_models: List[rebel.RBLNCompiledModel], rbln_device_map: Dict[str, int]
    ) -> List[rebel.Runtime]:
        device_val = rbln_device_map[DEFAULT_COMPILED_MODEL_NAME]
        return [
            compiled_models[0].create_runtime("encoder", tensor_type="pt", device=device_val),
            compiled_models[0].create_runtime("decoder", tensor_type="pt", device=device_val),
        ]

    def can_generate(self):
        return True

    def get_encoder(self):
        return self.encoder

    def get_decoder(self):
        return self.decoder

    def prepare_inputs_for_generation(
        self,
        input_ids,
        attention_mask=None,
        decoder_attention_mask=None,
        **kwargs,
    ):
        cur_seq_len = input_ids.shape[-1]
        cache_position = cur_seq_len - 1
        max_seq_len = self.rbln_config.model_cfg["dec_max_seq_len"]
        decoder_batch_size = input_ids.shape[0]
        input_ids = input_ids[:, cur_seq_len - 1 : cur_seq_len].contiguous()
        decoder_attention_mask = torch.zeros(decoder_batch_size, max_seq_len, dtype=torch.float32)
        decoder_attention_mask[:, :cur_seq_len] = 1

        return {
            "decoder_input_ids": input_ids,
            "attention_mask": attention_mask.to(torch.float32),
            "decoder_attention_mask": decoder_attention_mask,
            "cache_position": cache_position,
        }

    def forward(
        self,
        input_ids: torch.LongTensor = None,
        cache_position: Union[List[torch.Tensor], torch.Tensor] = None,
        **kwargs,
    ) -> Tuple[torch.FloatTensor]:
        # common decoder
        cache_position = torch.full((self.rbln_config.model_cfg["batch_size"], 1), cache_position, dtype=torch.int32)
        logits = self._forward_decoder(input_ids=input_ids, cache_position=cache_position, **kwargs).logits

        return Seq2SeqLMOutput(
            logits=logits,
        )

    def _forward_decoder(
        self,
        attention_mask: Optional[torch.FloatTensor] = None,
        decoder_input_ids: Optional[torch.LongTensor] = None,
        decoder_attention_mask: Optional[torch.BoolTensor] = None,
        cache_position: Optional[torch.Tensor] = None,
        **kwargs,
    ) -> Tuple[torch.FloatTensor]:
        dec_attention_mask = decoder_attention_mask.clone()
        for b_idx in range(self.rbln_config.model_cfg["batch_size"]):
            dec_attention_mask[b_idx, : cache_position[b_idx] + 1] = 1

        decoder_output = self.decoder(
            input_ids=decoder_input_ids,
            attention_mask=dec_attention_mask,
            encoder_attention_mask=attention_mask,
            cache_position=cache_position,
            batch_position=torch.tensor(0, dtype=torch.int32),
        )
        lm_logits = decoder_output.logits[0]

        return Seq2SeqLMOutput(logits=lm_logits)

    def vllm_forward(
        self,
        input_ids: torch.LongTensor = None,
        cache_position: Union[List[torch.Tensor], torch.Tensor] = None,  # vllm keyword argument
        batch_idx: Optional[torch.LongTensor] = None,
        enc_lengths: List[int] = None,  # vllm return current attention_mask length
        **kwargs,
    ) -> Tuple[torch.FloatTensor]:
        # When using vllm, need the output of the encoder (ex. vocab_size + 100) and use that value act as start_token_id in decoder (ex. vocab_size + 99)
        # encoder
        if batch_idx is not None:
            enc_attention_mask = torch.zeros(1, self.rbln_config.model_cfg["enc_max_seq_len"], dtype=torch.float32)
            enc_attention_mask[0][: enc_lengths[batch_idx] + 1] = 1
            padding_need = self.rbln_config.model_cfg["enc_max_seq_len"] - input_ids.shape[-1]
            input_ids = torch.nn.functional.pad(input_ids, (0, padding_need))
            _ = self.encoder(input_ids, enc_attention_mask, batch_idx=batch_idx.to(torch.int32))
            logits = torch.zeros(1, 1, self.config.vocab_size + 100)
            logits[0][0][-1] = 1
        # decoder
        else:
            input_ids[input_ids == (self.config.vocab_size + 99)] = self.config.decoder_start_token_id
            cache_position[cache_position != 0] = cache_position[cache_position != 0] - 2

            enc_attention_mask = torch.zeros(
                self.rbln_config.model_cfg["batch_size"],
                self.rbln_config.model_cfg["enc_max_seq_len"],
                dtype=torch.float32,
            )
            dec_attention_mask = torch.zeros(
                self.rbln_config.model_cfg["batch_size"],
                self.rbln_config.model_cfg["dec_max_seq_len"],
                dtype=torch.float32,
            )
            for batch_idx in range(self.rbln_config.model_cfg["batch_size"]):
                enc_attention_mask[batch_idx, : enc_lengths[batch_idx] + 1] = 1

            logits = self._forward_decoder(
                attention_mask=enc_attention_mask,
                decoder_input_ids=input_ids,
                decoder_attention_mask=dec_attention_mask,
                cache_position=cache_position,
            ).logits

        return Seq2SeqLMOutput(logits=logits)

    def _prepare_encoder_decoder_kwargs_for_generation(
        self,
        inputs_tensor: torch.Tensor,
        model_kwargs,
        model_input_name: Optional[str] = None,
        generation_config: Optional[GenerationConfig] = None,
    ) -> Dict[str, Any]:
        # 1. get encoder
        encoder = self.get_encoder()

        # 2. Prepare encoder args and encoder kwargs from model kwargs.
        irrelevant_prefix = ["decoder_", "cross_attn", "use_cache"]
        encoder_kwargs = {
            argument: value
            for argument, value in model_kwargs.items()
            if not any(argument.startswith(p) for p in irrelevant_prefix)
        }
        encoder_signature = set(inspect.signature(encoder.forward).parameters)
        encoder_accepts_wildcard = "kwargs" in encoder_signature or "model_kwargs" in encoder_signature
        if not encoder_accepts_wildcard:
            encoder_kwargs = {
                argument: value for argument, value in encoder_kwargs.items() if argument in encoder_signature
            }

        batch_size, input_len = inputs_tensor.shape
        inputs_tensor = torch.nn.functional.pad(
            inputs_tensor,
            (0, self.rbln_config.model_cfg["enc_max_seq_len"] - input_len),
            value=self.rbln_config.model_cfg["pad_token_id"],
        )
        model_kwargs["attention_mask"] = torch.nn.functional.pad(
            model_kwargs["attention_mask"], (0, self.rbln_config.model_cfg["enc_max_seq_len"] - input_len)
        )

        # 3. make sure that encoder returns `ModelOutput`
        model_input_name = model_input_name if model_input_name is not None else self.main_input_name
        encoder_kwargs["return_dict"] = True
        encoder_kwargs["output_hidden_states"] = False
        encoder_kwargs["output_attentions"] = False

        for b in range(batch_size):
            batch_idx = torch.tensor(b, dtype=torch.int32)
            encoder_kwargs["input_ids"] = inputs_tensor[b].unsqueeze(0)
            encoder_kwargs["attention_mask"] = model_kwargs["attention_mask"][b].unsqueeze(0).to(torch.float32)
            model_kwargs["encoder_outputs"] = encoder(**encoder_kwargs, batch_idx=batch_idx)

        return model_kwargs
