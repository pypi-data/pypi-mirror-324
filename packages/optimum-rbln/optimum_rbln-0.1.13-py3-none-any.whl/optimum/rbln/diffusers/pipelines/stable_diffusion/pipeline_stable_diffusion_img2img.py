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
"""RBLNStableDiffusionPipeline class for inference of diffusion models on rbln devices."""

from diffusers import StableDiffusionImg2ImgPipeline

from ....modeling_diffusers import RBLNDiffusionMixin


class RBLNStableDiffusionImg2ImgPipeline(RBLNDiffusionMixin, StableDiffusionImg2ImgPipeline):
    """
    Pipeline for image-to-image generation using Stable Diffusion.

    This model inherits from [`StableDiffusionPipeline`]. Check the superclass documentation for the generic methods
    implemented for all pipelines (downloading, saving, running on a particular device, etc.).

    It implements the methods to convert a pre-trained Stable Diffusion pipeline into a RBLNStableDiffusion pipeline by:
    - transferring the checkpoint weights of the original into an optimized RBLN graph,
    - compiling the resulting graph using the RBLN compiler.
    """

    original_class = StableDiffusionImg2ImgPipeline
    _submodules = ["text_encoder", "unet", "vae"]
