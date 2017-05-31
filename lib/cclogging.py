# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

from .config import ConfigManager


def get_logger_for_name(name):
    """
    Create and return a logger for the given name space.
    :param name: The name space to create the logger for.
    :return: The logger created for the given name space.
    """
    logger = logging.getLogger(name)
    logger.setLevel(ConfigManager.LOGGING_LEVEL)
    formatter = LavaLogFormatter()
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


class LavaLogFormatter(logging.Formatter):
    """
    This class handles formatting logs.
    """

    BLUE = "\033[94m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    NONE = "\033[0m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    YELLOW = "\033[33m"

    CRITICAL = RED + "%(asctime)s [ C ] %(message)s" + NONE
    ERROR = "%(asctime)s [" + RED + " E " + NONE + "] %(message)s"
    WARNING = "%(asctime)s [" + YELLOW + " W " + NONE + "] %(message)s"
    INFO = "%(asctime)s [" + GREEN + " I " + NONE + "] %(message)s"
    DEBUG = "%(asctime)s [" + BLUE + " D " + NONE + "] %(message)s"

    def __init__(self):
        super(LavaLogFormatter, self).__init__(datefmt="[%m/%d %H:%M:%S]")

    def format(self, record):
        """
        Format the contents of the given record to log.
        :param record: The record to log.
        :return: Results of calling super.format.
        """
        if record.levelno == logging.CRITICAL:
            self._fmt = LavaLogFormatter.CRITICAL
        elif record.levelno == logging.ERROR:
            self._fmt = LavaLogFormatter.ERROR
        elif record.levelno == logging.WARNING:
            self._fmt = LavaLogFormatter.WARNING
        elif record.levelno == logging.INFO:
            self._fmt = LavaLogFormatter.INFO
        elif record.levelno == logging.DEBUG:
            self._fmt = LavaLogFormatter.DEBUG
        return super(LavaLogFormatter, self).format(record)
