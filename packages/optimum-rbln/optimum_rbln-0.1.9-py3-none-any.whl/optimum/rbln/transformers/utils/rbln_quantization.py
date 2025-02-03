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


from typing import Any, List

import torch
from torch.nn import Linear, Parameter
from torch.nn import functional as F


QUANTIZED_WEIGHTS = [
    "q_proj",
    "k_proj",
    "v_proj",
    "o_proj",
    "gate_proj",
    "up_proj",
    "down_proj",
]


def replace_quantized_linear_layers(
    module: torch.nn.Module,
) -> None:
    """Replace target(quantized) linear layer's forward to qlinear forward

    Args:
        module (torch.nn.Module): The module containing the linear layers to be replaced.
                                  For example, this could be an instance of a model like
                                  LlamaForCausalLM().
    """
    processed_names: List[str] = []

    for name, layer in module.named_modules():
        is_replace_linear = name.split(".")[-1] in QUANTIZED_WEIGHTS
        if isinstance(layer, torch.nn.Linear) and is_replace_linear:
            *parent_address, child_name = name.split(".")
            parent = access_attribute(module, parent_address)
            setattr(parent, child_name, get_qlinear(layer))
            processed_names.append(name)
    names_repr = ", ".join(processed_names)
    print(f"Replace the following linear layers as qlinear layer:\n {{{names_repr}}}")


def access_attribute(obj: Any, tokens: List[str]) -> Any:
    """Get attribute of given object.

    Args:
        obj: object

        tokens (List[str]): attribute names to access, must be in correct order

    Returns:
        Any: accessed attribute

    Raises:
        AttributeError: If attribute doesn't exists
    """
    if len(tokens) == 0:
        return obj
    return access_attribute(getattr(obj, tokens[0]), tokens[1:])


def get_qlinear(layer: Linear):
    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        """Perform weight-only quantized linear layer.

        Forward workflow:
          - cast weight to high precision
          - multiply scale factor to weight
          - call torch.nn.functional linear
        Note:
          - Please don't modify following workflow
          - if the workflow must be changed please contact Rebellions
        """
        if inputs.dtype != self.scales.dtype:
            raise TypeError(f"Expected tensor of dtype {self.scales.dtype} but got {inputs.dtype}")
        w_fp = self.weight.type(inputs.dtype)
        w_fp *= self.scales.view(-1, 1)
        return F.linear(inputs, w_fp, self.bias)

    keep = layer.weight.to(torch.int8)
    layer.weight = None
    del layer.weight
    layer.weight = Parameter(keep, requires_grad=False)
    layer.scales = Parameter(torch.ones(layer.out_features, dtype=torch.float32), requires_grad=False)
    layer.forward = lambda *args, **kwargs: forward(layer, *args, **kwargs)
    return layer
