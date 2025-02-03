import os
from datetime import datetime

from halo import Halo

from .logging import get_logger


logger = get_logger()


def rbln_timer(print_name):
    def decorator(function):
        def wrapper(*args, **kwargs):
            disable = os.getenv("OPTIMUM_RBLN_DISABLE_SPIN", "False").lower() in ("true", "1", "t")
            if disable:
                logger.info(f"{print_name} ...")

            spinner = Halo(text=f"{print_name} ...", spinner="dots", color="green", enabled=(not disable))
            spinner.start()

            # Start timer
            tick = datetime.now()
            try:
                result = function(*args, **kwargs)
            except Exception as e:
                spinner.fail(f"{print_name} failed.")
                raise e

            # Print elapsed time.
            if disable:
                logger.info(f"{print_name} done. Elasped time: {format_elapsed_time(tick)}")

            spinner.stop()
            spinner.succeed(text=f"{print_name} done. Elasped time: {format_elapsed_time(tick)}")
            return result

        return wrapper

    def format_elapsed_time(start_time: datetime) -> str:
        return str(datetime.now() - start_time)[:7]

    return decorator
