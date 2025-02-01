""" Logger utilities """

import logging

logging.basicConfig(format="%(asctime)s %(message)s")


def get_logger():
    """Get logger with common formatting"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    return logger


def format_log_level(log_level: str):
    if log_level == "WARN":
        log_level = "warning"

    return log_level.lower()
