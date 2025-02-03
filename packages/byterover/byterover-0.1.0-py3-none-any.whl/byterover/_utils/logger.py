import logging
import os


def configure_logger(logger: logging.Logger, log_level: str, log_format: str):
    ch = logging.StreamHandler()
    log_level_numeric = logging.getLevelName(log_level.upper())
    logger.setLevel(log_level_numeric)
    ch.setLevel(log_level_numeric)
    ch.setFormatter(logging.Formatter("[%(threadName)s] %(asctime)s %(message)s", datefmt="%Y-%m-%dT%H:%M:%S%z"))

    logger.addHandler(ch)


log_level = os.environ.get("BYTEROVER_LOGLEVEL", "WARNING")
log_format = os.environ.get("BYTEROVER_LOG_FORMAT", "STRING")

logger = logging.getLogger("byterover-_utils")
configure_logger(logger, log_level, log_format)
