# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

from .resultfile import CCResultFileParser
from ..config import ConfigManager
from ..cclogging import get_logger_for_name

logger = get_logger_for_name(__name__)


class CCResultParser(object):
    """
    This is a class for parsing the contents of all lavalamp Common Crawl results file in a given
    directory.
    """

    # Class Members

    # Instantiation

    def __init__(self, directory_path):
        self._directory_path = directory_path

    # Static Methods

    # Class Methods

    # Public Methods

    def process_files_in_directory(
            self,
            ignore_threshold=ConfigManager.IGNORE_THRESHOLD,
            report_interval=ConfigManager.REPORT_INTERVAL,
            output_directory=ConfigManager.OUTPUT_DIRECTORY,
    ):
        """
        Process all of the result files in self.directory_path.
        :param ignore_threshold: The minimum count that should be admonished when processing
        contents of the results file.
        :param report_interval: The interval upon which to report to the user that processing is continuing.
        :param output_directory: The directory where results should be stored.
        :return: None
        """
        for file_name in os.listdir(self.directory_path):
            if file_name.startswith(ConfigManager.RESULT_FILE_PREAMBLE):
                file_path = os.path.join(self.directory_path, file_name)
                self.process_file(
                    file_path=file_path,
                    ignore_threshold=ignore_threshold,
                    report_interval=report_interval,
                    output_directory=output_directory,
                )

    def process_file(
            self,
            file_path=None,
            ignore_threshold=ConfigManager.IGNORE_THRESHOLD,
            report_interval=ConfigManager.REPORT_INTERVAL,
            output_directory=ConfigManager.OUTPUT_DIRECTORY,
    ):
        """
        Process the contents of the file at the given file path.
        :param file_path: The file path to the results file to parse.
        :param ignore_threshold: The minimum count that should be admonished when processing
        contents of the results file.
        :param report_interval: The interval upon which to report to the user that processing is continuing.
        :param output_directory: The directory where results should be stored.
        :return: None
        """
        logger.debug(
            "Now processing the contents of file at path %s."
            % (file_path,)
        )
        if not os.path.isdir(ConfigManager.OUTPUT_DIRECTORY):
            os.makedirs(ConfigManager.OUTPUT_DIRECTORY)
        file_parser = CCResultFileParser(file_path)
        processed_count = ignored_count = 0
        for index, entry in enumerate(file_parser.iter_entries()):
            if not index % report_interval:
                logger.debug(
                    "On entry %s in file %s. %s processed, %s ignored."
                    % (index, file_path, processed_count, ignored_count)
                )
            if entry.count < ignore_threshold:
                ignored_count += 1
            else:
                self.__parse_entry(entry=entry, output_directory=output_directory)
                processed_count += 1

    # Protected Methods

    # Private Methods

    def __parse_entry(self, entry=None, output_directory=ConfigManager.OUTPUT_DIRECTORY):
        """
        Parse the contents of the given CCResultEntry and add the relevant contents to the expected
        directory.
        :param entry: The entry to process.
        :param output_directory: The directory where results should be stored.
        :return: None
        """
        if entry.is_record_processed_type:
            logger.debug("Entry is record processed type. Ignoring.")
            return
        results_path = os.path.join(output_directory, entry.server_type)
        if not os.path.isdir(results_path):
            os.makedirs(results_path)
        if entry.is_server_name:
            results_file_path = os.path.join(results_path, ConfigManager.SERVER_COUNT_FILE_NAME)
            with open(results_file_path, "w+") as f:
                f.write(str(entry.count))
        elif entry.is_server_path:
            url_segment = entry.url_path.replace("\t", "").strip()
            if not url_segment:
                return
            file_entry = "%s\t%s" % (url_segment, entry.count)
            results_file_path = os.path.join(results_path, ConfigManager.URL_PATH_FILE_NAME)
            with open(results_file_path, "a+") as f:
                f.write("%s\n" % file_entry)

    # Properties

    @property
    def directory_path(self):
        """
        Get the local file path to where the Common Crawl results files reside.
        :return: the local file path to where the Common Crawl results files reside.
        """
        return self._directory_path

    # Representation and Comparison

    def __repr__(self):
        return "<%s - %s>" % (self.__class__.__name__, self.directory_path)
