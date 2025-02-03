from functools import wraps

from .logging import get_logger


logger = get_logger(__name__)


def remove_compile_time_kwargs(func):
    """
    Decorator to handle compile-time parameters during inference.

    For RBLN-optimized pipelines, several parameters must be determined during compilation
    and cannot be modified during inference. This decorator:
    1. Removes and warns about LoRA scale in cross_attention_kwargs
    2. Removes and warns about image dimension parameters (height, width)

    Args:
        func: The pipeline's __call__ method to be wrapped
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        height_exists = "height" in kwargs and kwargs["height"] is not None
        width_exists = "width" in kwargs and kwargs["width"] is not None
        compiled_image_size = self.vae.image_size
        if height_exists or width_exists:
            if kwargs["height"] == compiled_image_size[0] and kwargs["width"] == compiled_image_size[1]:
                pass
            else:
                logger.warning(
                    "Image dimension parameters (`height`, `width`) will be ignored during inference. "
                    "Image dimensions must be specified during model compilation using from_pretrained()."
                )
                kwargs.pop("width", None)
                kwargs.pop("height", None)

        if "cross_attention_kwargs" in kwargs:
            cross_attention_kwargs = kwargs.get("cross_attention_kwargs")
            if not cross_attention_kwargs:
                return func(self, *args, **kwargs)

            has_scale = "scale" in cross_attention_kwargs
            if has_scale:
                logger.warning(
                    "LoRA scale in cross_attention_kwargs will be ignored during inference. "
                    "To adjust LoRA scale, specify it during model compilation using from_pretrained()."
                )

                # If scale is the only key, set to None
                # Otherwise, remove scale and preserve other settings
                if len(cross_attention_kwargs) == 1:
                    kwargs["cross_attention_kwargs"] = None
                else:
                    kwargs["cross_attention_kwargs"].pop("scale")

        return func(self, *args, **kwargs)

    return wrapper
