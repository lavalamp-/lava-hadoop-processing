# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging


class ConfigManager(object):
    """
    This class contains all configuration values for the project.
    """

    OUTPUT_DIRECTORY = "parsed_results"
    IGNORE_THRESHOLD = 100
    REPORT_INTERVAL = 100000
    SERVER_COUNT_FILE_NAME = "entry_count"
    URL_PATH_FILE_NAME = "url_segments"
    RESULT_FILE_PREAMBLE = "part-"
    HIT_LIST_FILE_PREAMBLE = "hit_list_"
    LOGGING_LEVEL = logging.DEBUG
    DEFAULT_THRESHOLDS = [50, 75, 90, 95, 99, 99.7, 99.9]
