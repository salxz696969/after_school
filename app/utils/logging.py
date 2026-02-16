import logging

import colorlog


def setup_logging() -> None:
    handler = colorlog.StreamHandler()  # type: ignore
    handler.setFormatter(  # type: ignore
        colorlog.ColoredFormatter(  # type: ignore
            "%(log_color)s%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            log_colors={
                "DEBUG": "cyan",
            },
        )
    )

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)  # type: ignore
    root_logger.setLevel(logging.DEBUG)
