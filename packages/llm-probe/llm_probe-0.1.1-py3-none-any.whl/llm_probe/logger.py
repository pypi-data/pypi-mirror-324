##########################################################################
##  Logger for LLM Probe Framework
##
##  Authors:  Junsoo    Kim   ( js.kim@hyperaccel.ai                )
##  Version:  0.0.1
##  Date:     2024-11-05      ( v0.0.1, init                        )
##
##########################################################################

import logging
from typing import Any, Literal

##########################################################################
## Class
##########################################################################


class CustomLogFormatter(logging.Formatter):
    def __init__(self) -> None:
        super().__init__()
        self.default_format = "[%(asctime)s] [%(levelname)s] %(message)s"
        self.datefmt = "%Y-%m-%d %H:%M:%S"

    def format(self, record: Any) -> str:
        # Set log level to lowercase
        record.levelname = record.levelname.lower()
        # Set log format color to green for INFO level
        log_fmt = self.default_format
        # Set log format and return
        formatter = logging.Formatter(log_fmt, self.datefmt)
        return formatter.format(record)


##########################################################################
## Function
##########################################################################


def get_logger(name: str, level: Literal["debug", "info"] = "info") -> logging.Logger:
    # Create logger
    logger = logging.getLogger(name)
    # Prevent duplication of handlers
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = CustomLogFormatter()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        # Set log level
        if level == "debug":
            logger.setLevel(logging.DEBUG)
        elif level == "info":
            logger.setLevel(logging.INFO)
    # Return logger
    return logger


##########################################################################
