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

import logging
from typing import TYPE_CHECKING, Iterable, Optional, Union

from transformers import AutoModelForDepthEstimation
from transformers.modeling_outputs import DepthEstimatorOutput

from ....modeling_base import RBLNModel
from ....modeling_config import RBLNConfig, RBLNRuntimeConfig


logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from transformers import AutoFeatureExtractor, AutoProcessor, AutoTokenizer, PretrainedConfig


class RBLNDPTForDepthEstimation(RBLNModel):
    model_type = "rbln_model"
    auto_model_class = AutoModelForDepthEstimation
    main_input_name = "pixel_values"

    @classmethod
    def _get_rbln_config(
        cls,
        preprocessors: Optional[Union["AutoFeatureExtractor", "AutoProcessor", "AutoTokenizer"]],
        model_config: Optional["PretrainedConfig"] = None,
        rbln_image_size: Optional[int] = None,
        rbln_batch_size: Optional[int] = None,
    ) -> RBLNConfig:
        if rbln_batch_size is None:
            rbln_batch_size = 1

        if rbln_image_size is None:
            for processor in preprocessors:
                image_size = getattr(processor, "size", None)

                if image_size is not None:
                    if isinstance(image_size, Iterable):
                        if "shortest_edge" in image_size:
                            rbln_image_size = image_size["shortest_edge"]
                            break
                        elif "height" in image_size and "width" in image_size:
                            rbln_image_size = image_size["height"], image_size["width"]
                            break
                    else:
                        rbln_image_size = image_size

            if rbln_image_size is None:
                rbln_image_size = getattr(model_config, "image_size", None)

            if rbln_image_size is None:
                raise ValueError("`rbln_image_size` should be specified!")

        if isinstance(rbln_image_size, int):
            rbln_image_size = rbln_image_size, rbln_image_size

        input_info = [("pixel_values", [rbln_batch_size, 3, rbln_image_size[0], rbln_image_size[1]], "float32")]

        rbln_runtime_config = RBLNRuntimeConfig(input_info=input_info)
        meta = {"rbln_image_size": rbln_image_size}

        return RBLNConfig.from_rbln_runtime_configs([rbln_runtime_config], _rbln_meta=meta)

    def forward(self, *args, **kwargs):
        predicted_depth = super().forward(*args, **kwargs)
        return DepthEstimatorOutput(predicted_depth=predicted_depth)
