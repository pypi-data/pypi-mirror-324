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
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Union

import rebel
import torch
from optimum.exporters import TasksManager
from transformers import (
    AutoModelForSpeechSeq2Seq,
    AutoProcessor,
    GenerationMixin,
    PretrainedConfig,
    WhisperForConditionalGeneration,
    WhisperModel,
)
from transformers.modeling_outputs import BaseModelOutput, Seq2SeqLMOutput

from ....modeling_base import RBLNBaseModel
from ....modeling_config import DEFAULT_COMPILED_MODEL_NAME, RBLNConfig, RBLNRuntimeConfig
from ....utils.runtime_utils import RBLNPytorchRuntime
from ....utils.save_utils import maybe_save_preprocessors
from .whisper_architecture import (
    _WhisperDecoderWrapper,
    _WhisperEncoderWrapper,
)


logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from transformers import (
        AutoFeatureExtractor,
        AutoProcessor,
        PretrainedConfig,
    )


class RBLNRuntimeEncoder(RBLNPytorchRuntime):
    mandatory_members = ["main_input_name"]

    def forward(self, *args: List[torch.Tensor], **kwargs: Dict[str, torch.Tensor]):
        _ = super().forward(input_features=kwargs["input_features"])
        return BaseModelOutput(last_hidden_state=torch.tensor([1.0]))


class RBLNRuntimeDecoder(RBLNPytorchRuntime):
    mandatory_members = ["main_input_name"]

    def forward(self, *args: List[torch.Tensor], **kwargs: Dict[str, torch.Tensor]):
        outputs = super().forward(*args, **kwargs)
        return Seq2SeqLMOutput(logits=outputs)


class RBLNWhisperForConditionalGeneration(RBLNBaseModel, GenerationMixin):
    """
    The Whisper Model with a language modeling head. Can be used for automatic speech recognition.
    This model inherits from [`RBLNBaseModel`]. Check the superclass documentation for the generic methods the library implements for all its models.

    A class to convert and run pre-trained transformers based LlamaForCausalLM model on RBLN devices.
    It implements the methods to convert a pre-trained transformers LlamaForCausalLM model into a RBLN transformer model by:
    - transferring the checkpoint weights of the original into an optimized RBLN graph,
    - compiling the resulting graph using the RBLN compiler.
    """

    model_type = "rbln_model"
    auto_model_class = AutoModelForSpeechSeq2Seq
    main_input_name = "input_ids"

    def __post_init__(self, **kwargs):
        self.batch_size = self.rbln_config[DEFAULT_COMPILED_MODEL_NAME][0].batch_size
        self.enc_max_seq_len = self.rbln_config.meta["input_max_length"]
        self.dec_max_seq_len = self.rbln_config.meta["rbln_dec_max_seq_len"]

        self.encoder = RBLNRuntimeEncoder(runtime=self.runtimes[0], main_input_name="input_features")
        self.decoder = RBLNRuntimeDecoder(runtime=self.runtimes[1], main_input_name="input_ids")
        self.forced_decoder_ids = self.config.forced_decoder_ids

        # used in GenerationMixin.generate()
        self.model = WhisperModel(self.config)
        self.pad_token_id = self.config.pad_token_id

    def can_generate(self):
        return True

    def get_encoder(self):
        return self.encoder

    def get_decoder(self):
        return self.decoder

    def __getattr__(self, __name: str) -> Any:
        """This is the key method to implement RBLN-Whisper.
        Returns:
            Any: Whisper's corresponding method
        """

        def redirect(func):
            return lambda *pargs, **kwargs: func(self, *pargs, **kwargs)

        val = getattr(WhisperForConditionalGeneration, __name)
        if isinstance(val, Callable) and "self" in set(inspect.signature(val).parameters):
            return redirect(val)
        return val

    def _reorder_cache(self, past_key_values, beam_idx):
        # TODO(jongho): implement
        raise NotImplementedError

    def prepare_inputs_for_generation(
        self,
        input_ids,
        decoder_attention_mask=None,
        input_features=None,  # Must be explicit
        **kwargs,
    ):
        max_seq_len = self.dec_max_seq_len
        cur_seq_len = input_ids.shape[-1]
        input_ids = input_ids[:, cur_seq_len - 1 : cur_seq_len].contiguous()
        decoder_attention_mask = torch.zeros(self.batch_size, max_seq_len, dtype=torch.int64)
        decoder_attention_mask[:, :cur_seq_len] = 1
        cache_position = torch.tensor(cur_seq_len - 1, dtype=torch.int32)

        return {
            "decoder_input_ids": input_ids,
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
    ) -> "RBLNWhisperForConditionalGeneration":
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

        model: WhisperForConditionalGeneration = TasksManager.get_model_from_task(
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

        def compile_whisper():
            wrapped_encoder = _WhisperEncoderWrapper(model).eval()
            wrapped_decoder = _WhisperDecoderWrapper(model).eval()

            enc_rbln_runtime_config = rbln_config[DEFAULT_COMPILED_MODEL_NAME][0]
            dec_rbln_runtime_config = rbln_config[DEFAULT_COMPILED_MODEL_NAME][1]

            enc_example_inputs = enc_rbln_runtime_config.get_dummy_inputs(fill=1)
            dec_example_inputs = dec_rbln_runtime_config.get_dummy_inputs(fill=1)

            enc_scripted_model = torch.jit.trace(wrapped_encoder, enc_example_inputs[0]).eval()
            dec_scripted_model = torch.jit.trace(wrapped_decoder, dec_example_inputs).eval()

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
            dec_ir.batch_size = dec_rbln_runtime_config.batch_size

            # Caching encoder/decoder I/O
            connections = [
                (enc_ir.outputs[0], dec_ir.inputs[4]),
                (dec_ir.outputs[1], dec_ir.inputs[3]),
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

        compile_whisper()
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
        preprocessors: Union["AutoFeatureExtractor", "AutoProcessor"],
        model_config: "PretrainedConfig",
        rbln_batch_size: Optional[int] = None,
    ) -> RBLNConfig:
        meta = {}

        input_max_length = 3000
        rbln_enc_num_mel_bins = getattr(model_config, "num_mel_bins", None)
        if rbln_enc_num_mel_bins is None:
            for feature_extractor in preprocessors:
                if hasattr(feature_extractor, "feature_size"):
                    rbln_enc_num_mel_bins = feature_extractor.feature_size
                    break
            raise ValueError("`rbln_enc_num_mel_bins` should be specified!")

        rbln_enc_max_seq_len = getattr(model_config, "max_source_positions", None)
        if rbln_enc_max_seq_len is None:
            raise ValueError("`rbln_enc_max_seq_len` should be specified!")

        rbln_dec_max_seq_len = getattr(model_config, "max_length", None)
        if rbln_dec_max_seq_len is None:
            raise ValueError("`rbln_dec_max_seq_len` should be specified!")

        rbln_batch_size = 1 if rbln_batch_size is None else rbln_batch_size
        decoder_batch_size = rbln_batch_size

        meta["rbln_dec_max_seq_len"] = rbln_dec_max_seq_len
        meta["rbln_enc_max_seq_len"] = rbln_enc_max_seq_len
        meta["num_mel_bins"] = rbln_enc_num_mel_bins
        meta["input_max_length"] = input_max_length
        meta["decoder_batch_size"] = decoder_batch_size
        meta["forced_decoder_ids"] = model_config.forced_decoder_ids

        # model input info
        enc_input_info = [("input_features", [rbln_batch_size, rbln_enc_num_mel_bins, input_max_length], "float32")]
        dec_input_info = [
            ("decoder_input_ids", [decoder_batch_size, 1], "int64"),
            ("decoder_attention_mask", [decoder_batch_size, rbln_dec_max_seq_len], "int64"),
            ("cache_position", [], "int32"),
        ]
        dec_input_info.extend(
            [
                (
                    "self_key_value_states",
                    [
                        model_config.decoder_layers * 2,
                        decoder_batch_size,
                        model_config.decoder_attention_heads,
                        rbln_dec_max_seq_len,
                        model_config.d_model // model_config.encoder_attention_heads,
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
                        model_config.decoder_layers * 2,
                        rbln_batch_size,
                        model_config.decoder_attention_heads,
                        rbln_enc_max_seq_len,
                        model_config.d_model // model_config.encoder_attention_heads,
                    ],
                    "float32",
                )
            ]
        )

        enc_rbln_runtime_config = RBLNRuntimeConfig(rbln_mod_name="encoder", input_info=enc_input_info)
        dec_rbln_runtime_config = RBLNRuntimeConfig(rbln_mod_name="decoder", input_info=dec_input_info)

        enc_rbln_runtime_config.batch_size = rbln_batch_size
        dec_rbln_runtime_config.batch_size = decoder_batch_size

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
        decoder_input_ids: Optional[torch.LongTensor] = None,
        decoder_attention_mask: Optional[torch.LongTensor] = None,
        cache_position: Optional[torch.Tensor] = None,
        **kwargs,
    ) -> Seq2SeqLMOutput:
        decoder_output = self.decoder(
            decoder_input_ids=decoder_input_ids,
            decoder_attention_mask=decoder_attention_mask,
            cache_position=cache_position,
        )
        lm_logits = decoder_output.logits

        return Seq2SeqLMOutput(logits=lm_logits)

    def __repr__(self):
        return repr(self.runtimes[0]) + "\n" + repr(self.runtimes[1])
