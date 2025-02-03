# coding=utf-8
# Copyright 2023 The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""RBLNStableDiffusionXLPipeline class for inference of diffusion models on rbln devices."""

from diffusers import StableDiffusionXLPipeline

from ....modeling_base import RBLNBaseModel
from ....transformers import RBLNCLIPTextModel, RBLNCLIPTextModelWithProjection
from ...models import RBLNAutoencoderKL, RBLNUNet2DConditionModel


class RBLNStableDiffusionXLPipeline(StableDiffusionXLPipeline):
    @classmethod
    def from_pretrained(cls, model_id, **kwargs):
        """
        Pipeline for text-to-image generation using Stable Diffusion XL.

        This model inherits from [`StableDiffusionXLPipeline`]. Check the superclass documentation for the generic methods the
        library implements for all the pipelines (such as downloading or saving, running on a particular device, etc.)

        It implements the methods to convert a pre-trained StableDiffusionXL pipeline into a RBLNStableDiffusionXL pipeline by:
        - transferring the checkpoint weights of the original into an optimized RBLN graph,
        - compiling the resulting graph using the RBLN compiler.

        Args:
            model_id (`Union[str, Path]`):
                Can be either:
                - A string, the *model id* of a pretrained model hosted inside a model repo on huggingface.co.
                - A path to a *directory* containing a model saved using [`~OptimizedModel.save_pretrained`],
        """
        export = kwargs.pop("export", None)
        model_save_dir = kwargs.pop("model_save_dir", None)
        rbln_config_kwargs, rbln_constructor_kwargs = RBLNBaseModel.pop_rbln_kwargs_from_kwargs(kwargs)
        model = super().from_pretrained(pretrained_model_name_or_path=model_id, **kwargs)

        if export is None or export is False:
            return model

        do_classifier_free_guidance = (
            rbln_config_kwargs.pop("rbln_guidance_scale", 5.0) > 1.0 and model.unet.config.time_cond_proj_dim is None
        )

        vae = RBLNAutoencoderKL.from_pretrained(
            model_id=model_id,
            subfolder="vae",
            export=True,
            model_save_dir=model_save_dir,
            rbln_unet_sample_size=model.unet.config.sample_size,
            rbln_use_encode=False,
            **rbln_config_kwargs,
            **rbln_constructor_kwargs,
        )
        text_encoder = RBLNCLIPTextModel.from_pretrained(
            model_id=model_id,
            subfolder="text_encoder",
            export=True,
            model_save_dir=model_save_dir,
            **rbln_config_kwargs,
            **rbln_constructor_kwargs,
        )
        text_encoder_2 = RBLNCLIPTextModelWithProjection.from_pretrained(
            model_id=model_id,
            subfolder="text_encoder_2",
            export=True,
            model_save_dir=model_save_dir,
            **rbln_config_kwargs,
            **rbln_constructor_kwargs,
        )

        batch_size = rbln_config_kwargs.pop("rbln_batch_size", 1)
        unet_batch_size = batch_size * 2 if do_classifier_free_guidance else batch_size

        unet = RBLNUNet2DConditionModel.from_pretrained(
            model_id=model_id,
            subfolder="unet",
            export=True,
            model_save_dir=model_save_dir,
            rbln_max_seq_len=model.text_encoder.config.max_position_embeddings,
            rbln_text_model_hidden_size=model.text_encoder_2.config.hidden_size,
            rbln_batch_size=unet_batch_size,
            rbln_use_encode=False,
            rbln_is_controlnet=True if "controlnet" in model.config.keys() else False,
            **rbln_config_kwargs,
            **rbln_constructor_kwargs,
        )

        if model_save_dir is not None:
            # To skip saving original pytorch modules
            del (model.vae, model.text_encoder, model.unet, model.text_encoder_2)

            # Direct calling of `save_pretrained` causes config.unet = (None, None).
            # So config must be saved again, later.
            model.save_pretrained(model_save_dir)

        model.vae = vae
        model.text_encoder = text_encoder
        model.unet = unet
        model.text_encoder_2 = text_encoder_2
        update_dict = {
            "vae": ("optimum.rbln", "RBLNAutoencoderKL"),
            "text_encoder": ("optimum.rbln", "RBLNCLIPTextModel"),
            "unet": ("optimum.rbln", "RBLNUNet2DConditionModel"),
            "text_encoder_2": ("optimum.rbln", "RBLNCLIPTextModel"),
        }
        model.register_to_config(**update_dict)

        if model_save_dir is not None:
            # overwrite to replace incorrect config
            model.save_config(model_save_dir)

        model.models = [vae.model[0], unet.model[0], text_encoder.model[0], text_encoder_2.model[0]]

        if rbln_constructor_kwargs.pop("rbln_optimize_host_memory", None) is False:
            model.compiled_models = [
                vae.compiled_models[0],
                unet.compiled_models[0],
                text_encoder.compiled_models[0],
                text_encoder_2.compiled_models[0],
            ]

        return model
