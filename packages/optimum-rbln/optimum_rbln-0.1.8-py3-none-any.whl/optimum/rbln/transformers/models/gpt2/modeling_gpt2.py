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
from typing import TYPE_CHECKING, Any, Callable, Optional, Union

from transformers import GPT2LMHeadModel, PretrainedConfig, PreTrainedModel

from ....modeling_config import RBLNConfig, RBLNRuntimeConfig
from ...models.decoderonly import RBLNDecoderOnlyModelForCausalLM
from .gpt2_architecture import GPT2LMHeadModelWrapper


logger = logging.getLogger(__name__)
if TYPE_CHECKING:
    from transformers import (
        AutoFeatureExtractor,
        AutoProcessor,
        AutoTokenizer,
        PretrainedConfig,
    )


class RBLNGPT2LMHeadModel(RBLNDecoderOnlyModelForCausalLM):
    """
    The GPT2 Model transformer with a language modeling head on top (linear layer with weights tied to the input
    embeddings).

    This model inherits from [`RBLNMultiModel`]. Check the superclass documentation for the generic methods the
    library implements for all its model.

    It implements the methods to convert a pre-trained transformers GPT2 model into a RBLN transformer model by:
    - transferring the checkpoint weights of the original into an optimized RBLN graph,
    - compiling the resulting graph using the RBLN compiler.

    """

    @classmethod
    def wrapping_torch_model(self, model: "PreTrainedModel", rbln_max_seq_len: int):
        return GPT2LMHeadModelWrapper(model, rbln_max_seq_len).eval()

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
        if rbln_max_seq_len is None:  # differenct from llama
            rbln_max_seq_len = getattr(model_config, "n_positions", None)
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
                else model_config.hidden_size // model_config.n_head
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
                            model_config.n_head,  # differenct from llama
                            rbln_max_seq_len,
                            head_dim,
                        ],
                        "float32",
                    )
                    for i in range(model_config.n_layer * 2)  # differenct from llama
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
