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
from transformers import (
    AutoModelForSeq2SeqLM,
    BartConfig,
    BartForConditionalGeneration,
    PretrainedConfig,
    T5ForConditionalGeneration,
)
from transformers.modeling_outputs import BaseModelOutput, Seq2SeqLMOutput

from .modeling_base import RBLNBaseModel
from .modeling_config import DEFAULT_COMPILED_MODEL_NAME, RBLNConfig, RBLNRuntimeConfig
from .transformers.models.bart import BartDecoderWrapper, BartEncoderWrapper
from .transformers.models.t5 import T5DecoderWrapper, T5EncoderWrapper
from .utils.runtime_utils import RBLNPytorchRuntime
from .utils.save_utils import maybe_save_preprocessors


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
        # Just indicates that it is not None
        return BaseModelOutput(last_hidden_state=torch.tensor([1.0]))


class RBLNRuntimeDecoder(RBLNPytorchRuntime):
    mandatory_members = ["main_input_name"]

    def forward(self, *args: List[torch.Tensor], **kwargs: Dict[str, torch.Tensor]):
        outputs = super().forward(*args, **kwargs)
        return Seq2SeqLMOutput(logits=outputs)


class RBLNModelForSeq2SeqLM(RBLNBaseModel):
    """
    This is a generic model class that will be instantiated as one of the model classes of the library (with a sequence-to-sequence language modeling head) when created with the from_pretrained() class method.
    This model inherits from [`RBLNBaseModel`]. Check the superclass documentation for the generic methods the library implements for all its models.

    A class to convert and run pre-trained transformers based Seq2SeqLM models on RBLN devices.
    It implements the methods to convert a pre-trained transformers Seq2SeqLM model into a RBLN transformer model by:
    - transferring the checkpoint weights of the original into an optimized RBLN graph,
    - compiling the resulting graph using the RBLN compiler.

    Currently, this model class only supports the 'bart' and 't5' models from the transformers library. Future updates may include support for additional model types.
    """

    model_type = "rbln_model"
    auto_model_class = AutoModelForSeq2SeqLM

    def __post_init__(self, **kwargs):
        self.model_dim = self.config.d_model
        self.batch_size = self.rbln_config[DEFAULT_COMPILED_MODEL_NAME][0].batch_size
        self.enc_max_seq_len = self.rbln_config.meta["rbln_enc_max_seq_len"]
        self.dec_max_seq_len = self.rbln_config.meta["rbln_dec_max_seq_len"]
        self.pad_token_id = self.rbln_config.meta["rbln_pad_token_id"]
        self.encoder = RBLNRuntimeEncoder(runtime=self.runtimes[0], main_input_name="input_ids")
        self.decoder = RBLNRuntimeDecoder(runtime=self.runtimes[1], main_input_name="input_ids")

    def can_generate(self):
        return True

    def get_encoder(self):
        return self.encoder

    def get_decoder(self):
        return self.decoder

    def __getattr__(self, __name: str) -> Any:
        def redirect(func):
            return lambda *pargs, **kwargs: func(self, *pargs, **kwargs)

        if "T5ForConditionalGeneration" == self.config.architectures:
            val = getattr(T5ForConditionalGeneration, __name)
        else:
            val = getattr(BartForConditionalGeneration, __name)

        if isinstance(val, Callable) and "self" in set(inspect.signature(val).parameters):
            return redirect(val)
        return val

    def prepare_inputs_for_generation(
        self,
        input_ids,
        past_key_values=None,
        attention_mask=None,
        decoder_attention_mask=None,
        **kwargs,
    ):
        max_seq_len = self.dec_max_seq_len
        cur_seq_len = input_ids.shape[-1]
        decoder_batch_size = input_ids.shape[0]
        input_ids = input_ids[:, cur_seq_len - 1 : cur_seq_len].contiguous()

        # In greedy decoding
        decoder_attention_mask = torch.zeros(decoder_batch_size, max_seq_len, dtype=torch.int64)
        decoder_attention_mask[:, :cur_seq_len] = 1
        cache_position = torch.tensor(cur_seq_len - 1, dtype=torch.int32)

        return {
            "decoder_input_ids": input_ids,
            "past_key_values": past_key_values,
            "attention_mask": attention_mask,
            "decoder_attention_mask": decoder_attention_mask,
            "cache_position": cache_position,
        }

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
    ) -> "AutoModelForSeq2SeqLM":
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
                "use_cache": False,
            }
        )

        rbln_config_kwargs, rbln_constructor_kwargs = cls.pop_rbln_kwargs_from_kwargs(kwargs)

        model: AutoModelForSeq2SeqLM = TasksManager.get_model_from_task(
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

        def optimized_models(model):
            if isinstance(model, T5ForConditionalGeneration):
                encoder_model = T5EncoderWrapper(model).eval()
                decoder_model = T5DecoderWrapper(model).eval()
            elif isinstance(model, BartForConditionalGeneration):
                encoder_model = BartEncoderWrapper(model).eval()
                decoder_model = BartDecoderWrapper(model).eval()
            else:
                raise ValueError(f"{model.__class__.__name__} is not supported yet.")

            return encoder_model, decoder_model

        def compile():
            wrapped_encoder, wrapped_decoder = optimized_models(model)

            wrapped_encoder.encoder_max_length = rbln_config.meta["rbln_enc_max_seq_len"]
            wrapped_encoder.decoder_max_length = rbln_config.meta["rbln_dec_max_seq_len"]
            wrapped_encoder.decoder_batch_size = rbln_config.meta["rbln_batch_size"]

            wrapped_decoder.encoder_max_length = rbln_config.meta["rbln_enc_max_seq_len"]
            wrapped_decoder.decoder_max_length = rbln_config.meta["rbln_dec_max_seq_len"]
            wrapped_decoder.decoder_batch_size = rbln_config.meta["rbln_batch_size"]

            enc_rbln_runtime_config = rbln_config[DEFAULT_COMPILED_MODEL_NAME][0]
            dec_rbln_runtime_config = rbln_config[DEFAULT_COMPILED_MODEL_NAME][1]

            if isinstance(model, T5ForConditionalGeneration):
                enc_example_inputs = enc_rbln_runtime_config.get_dummy_inputs(fill=1)
                dec_example_inputs = dec_rbln_runtime_config.get_dummy_inputs(fill=1)
            else:
                enc_example_inputs = enc_rbln_runtime_config.get_dummy_inputs(fill=0)
                dec_example_inputs = dec_rbln_runtime_config.get_dummy_inputs(fill=0)

            enc_scripted_model = torch.jit.trace(wrapped_encoder, enc_example_inputs)
            dec_scripted_model = torch.jit.trace(wrapped_decoder, dec_example_inputs)

            enc_ir = rebel.torchscript_to_ir(
                enc_scripted_model,
                input_names=[v[0] for v in enc_rbln_runtime_config.input_info],
                name=enc_rbln_runtime_config.rbln_mod_name,
            )
            dec_ir = rebel.torchscript_to_ir(
                dec_scripted_model,
                input_names=[v[0] for v in dec_rbln_runtime_config.input_info],
                name=dec_rbln_runtime_config.rbln_mod_name,
            )
            dec_ir.decoder_batch_size = rbln_config.meta["rbln_batch_size"]

            connections = [
                (enc_ir.outputs[0], dec_ir.inputs[5]),
                (dec_ir.outputs[1], dec_ir.inputs[4]),
            ]
            compiled_model = rebel.compile(
                enc_ir,
                dec_ir,
                connections=connections,
                fusion=enc_rbln_runtime_config.fusion,
                npu=enc_rbln_runtime_config.npu,
                tensor_parallel_size=enc_rbln_runtime_config.tensor_parallel_size,
            )
            compiled_model.save(save_dir_path / f"{DEFAULT_COMPILED_MODEL_NAME}.rbln")

        compile()

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
        rbln_enc_max_seq_len: Optional[int] = None,
        rbln_dec_max_seq_len: Optional[int] = None,
        rbln_batch_size: Optional[int] = 1,
    ) -> RBLNConfig:
        meta = {}

        if isinstance(model_config, BartConfig):
            n_layer = model_config.decoder_layers
            n_head = model_config.decoder_attention_heads
            d_kv = model_config.d_model // model_config.encoder_attention_heads
        else:
            n_layer = model_config.num_layers
            n_head = model_config.num_heads
            d_kv = model_config.d_kv

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

        rbln_batch_size = 1 if rbln_batch_size is None else rbln_batch_size

        meta["rbln_enc_max_seq_len"] = rbln_enc_max_seq_len
        meta["rbln_dec_max_seq_len"] = rbln_dec_max_seq_len
        meta["rbln_batch_size"] = rbln_batch_size
        meta["rbln_pad_token_id"] = rbln_pad_token_id

        # model input info
        enc_input_info = [
            ("input_ids", [rbln_batch_size, rbln_enc_max_seq_len], "int64"),
            ("attention_mask", [rbln_batch_size, rbln_enc_max_seq_len], "int64"),
        ]

        dec_input_info = [
            ("input_ids", [rbln_batch_size, 1], "int64"),
            ("attention_mask", [rbln_batch_size, rbln_dec_max_seq_len], "int64"),
            ("encoder_attention_mask", [rbln_batch_size, rbln_enc_max_seq_len], "int64"),
            (
                "cache_position",
                [],
                "int32",
            ),
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
        enc_rbln_runtime_config = RBLNRuntimeConfig(rbln_mod_name="encoder", input_info=enc_input_info)
        dec_rbln_runtime_config = RBLNRuntimeConfig(rbln_mod_name="decoder", input_info=dec_input_info)

        rbln_config = RBLNConfig.from_rbln_runtime_configs(
            [enc_rbln_runtime_config, dec_rbln_runtime_config],
            _rbln_meta=meta,
        )

        return rbln_config

    def _create_runtimes(self, rbln_device_map: Dict[str, int]) -> List[rebel.Runtime]:
        device_val = rbln_device_map[DEFAULT_COMPILED_MODEL_NAME]
        return [
            self.compiled_models[0].create_runtime("encoder", tensor_type="pt", device=device_val),
            self.compiled_models[0].create_runtime("decoder", tensor_type="pt", device=device_val),
        ]

    def forward(
        self,
        attention_mask: Optional[torch.FloatTensor] = None,
        decoder_input_ids: Optional[torch.LongTensor] = None,
        decoder_attention_mask: Optional[torch.BoolTensor] = None,
        cache_position: Optional[torch.Tensor] = None,
        **kwargs,
    ) -> Tuple[torch.FloatTensor]:
        decoder_output = self.decoder(
            input_ids=decoder_input_ids,
            attention_mask=decoder_attention_mask,
            encoder_attention_mask=attention_mask,
            cache_position=cache_position,
        )
        lm_logits = decoder_output.logits

        return Seq2SeqLMOutput(logits=lm_logits)

    def __repr__(self):
        return repr(self.runtimes[0]) + "\n" + repr(self.runtimes[1])

    def _prepare_encoder_decoder_kwargs_for_generation(
        self,
        inputs_tensor: torch.Tensor,
        model_kwargs,
        model_input_name: Optional[str] = None,
        *args,
        **kwargs,
    ) -> Dict[str, Any]:
        ########## thkim change start ###################
        # padding input_ids & attention_mask regardless of user's tokenizer usage
        batch_size, input_len = inputs_tensor.shape
        inputs_tensor = torch.nn.functional.pad(
            inputs_tensor, (0, self.enc_max_seq_len - input_len), value=self.pad_token_id
        )
        model_kwargs["attention_mask"] = torch.nn.functional.pad(
            model_kwargs["attention_mask"], (0, self.enc_max_seq_len - input_len), value=0
        )
        ########## thkim change end ###################

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

        # 3. make sure that encoder returns `ModelOutput`
        model_input_name = model_input_name if model_input_name is not None else self.main_input_name
        encoder_kwargs["return_dict"] = True
        encoder_kwargs[model_input_name] = inputs_tensor
        model_kwargs["encoder_outputs"] = encoder(**encoder_kwargs)

        return model_kwargs
