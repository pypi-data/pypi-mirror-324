import logging
import logging.handlers
from typing import Literal
from pathlib import Path


def special_logger(name: str, level: Literal[50, 40, 30, 20, 10, 0] = logging.INFO, to_console: bool = True):

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if Path("logs").exists():
        file_handler = logging.handlers.RotatingFileHandler(f"logs/{name}.log", maxBytes=5000000,
                                                            backupCount=10)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if to_console:
        console_out = logging.StreamHandler()
        logger.addHandler(console_out)

    return logger