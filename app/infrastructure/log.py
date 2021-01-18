import logging
from app.config import LOG_LEVEL


def configure_logging():
    if LOG_LEVEL == "DEBUG":
        log_format = "%(levelname)s - %(message)s - %(funcName)s - %(lineno)d"
        logging.basicConfig(level=LOG_LEVEL, format=log_format)
    else:
        logging.basicConfig(level=LOG_LEVEL)
