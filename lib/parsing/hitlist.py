# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import re

from ..cclogging import get_logger_for_name
from ..config import ConfigManager

logger = get_logger_for_name(__name__)


class HitListParser(object):
    """
    This class is responsible for generating hit lists by servers based on the parsed results
    from a lavalamp Common Crawl analysis.
    """

    # Class Members

    COERCED_REGEX = re.compile("\[\[.*?\]\]")

    # Instantiation

    def __init__(self, results_directory=ConfigManager.OUTPUT_DIRECTORY):
        self._results_directory = results_directory

    # Static Methods

    # Class Methods

    # Public Methods

    def generate_hit_lists_for_all_servers(
            self,
            thresholds=ConfigManager.DEFAULT_THRESHOLDS,
            hit_list_preamble=ConfigManager.HIT_LIST_FILE_PREAMBLE
    ):
        """
        Generate hit lists for all server types found in self.results_directory.
        :param thresholds: A list of thresholds to generate hit lists for.
        :param hit_list_preamble: The file name preamble to use for the hit list file that this method
        generates.
        :return: None
        """
        for server_type in os.listdir(self.results_directory):
            self.generate_hit_lists_for_server(
                server_type=server_type,
                thresholds=thresholds,
                hit_list_preamble=hit_list_preamble,
            )

    def generate_hit_lists_for_server(
            self,
            server_type=None,
            thresholds=ConfigManager.DEFAULT_THRESHOLDS,
            hit_list_preamble=ConfigManager.HIT_LIST_FILE_PREAMBLE
    ):
        """
        Generate hit lists for the given server type using the given thresholds.
        :param server_type: The server type string to generate the hit list for.
        :param thresholds: A list of thresholds to generate hit lists for.
        :param hit_list_preamble: The file name preamble to use for the hit list file that this method
        generates.
        :return: None
        """
        for threshold in thresholds:
            self.generate_hit_list_for_server(
                server_type=server_type,
                threshold=threshold,
                hit_list_preamble=hit_list_preamble,
            )

    def generate_hit_list_for_server(
            self,
            server_type=None,
            threshold=None,
            hit_list_preamble=ConfigManager.HIT_LIST_FILE_PREAMBLE,
    ):
        """
        Generate a hit list for the given server type based on the given threshold.
        :param server_type: The server type string to generate the hit list for.
        :param threshold: The coverage threshold to generate the hit list for.
        :param hit_list_preamble: The file name preamble to use for the hit list file that this method
        generates.
        :return: None
        """
        logger.debug(
            "Now generating hit list for server type %s. Threshold is %s."
            % (server_type, threshold)
        )
        hits_count = self.__get_total_hits_for_server_type(server_type=server_type)
        url_segments = self.__get_url_segments_for_server_type(server_type=server_type)
        logger.debug(
            "There were a total of %s hits for server type %s. Now processing %s URL segments to find threshold of %s."
            % (hits_count, server_type, len(url_segments), threshold)
        )
        coverage_count = 0
        threshold_percentage = 0.01 * threshold
        hit_list_segments = []
        for url_segment, segment_count in url_segments:
            hit_list_segments.append(url_segment)
            coverage_count += segment_count
            coverage_percent = float(coverage_count) / hits_count
            if coverage_percent >= threshold_percentage:
                break
        logger.debug(
            "To achieve coverage of %s for server %s, %s URL segments are required."
            % (threshold, server_type, len(hit_list_segments))
        )
        file_name = "%s%s" % (hit_list_preamble, threshold)
        file_path = os.path.join(self.results_directory, server_type, file_name)
        logger.debug(
            "Writing contents of hit list for server type %s and threshold %s to file %s."
            % (server_type, threshold, file_path)
        )
        with open(file_path, "w+") as f:
            f.write("\n".join(hit_list_segments))

    # Protected Methods

    # Private Methods

    def __get_total_hits_for_server_type(
            self,
            server_type=None,
            count_file_name=ConfigManager.SERVER_COUNT_FILE_NAME,
    ):
        """
        Get the total number of URL segments found for the given server type.
        :param server_type: A string depicting the server to retrieve the URL segments count for.
        :param count_file_name: The name of the file to retrieve the count from.
        :return: An integer representing the number of URL segments found for the given server type.
        """
        file_path = os.path.join(self.results_directory, server_type, count_file_name)
        with open(file_path, "r") as f:
            content = f.read().strip()
        return int(content)

    def __get_url_segments_for_server_type(
            self,
            server_type=None,
            segments_file_name=ConfigManager.URL_PATH_FILE_NAME,
            do_sort=True,
            filter_coerced=True,
    ):
        """
        Get a list of tuples containing all of the URL segments found for the given server type.
        :param server_type: A string depicting the server to retrieve the URL segments count for.
        :param segments_file_name: The name of the file to retrieve the segments from.
        :param do_sort: Whether or not to sort the results before returning them.
        :param filter_coerced: Whether or not to filter out URL segments that contain coerced values (ex:
        [[INTEGER]].
        :return: A list of tuples containing (1) the URL segment and (2) the count for all URL segments
        associated with the given server type.
        """
        logger.debug(
            "Now retrieving URL segments for server type %s."
            % (server_type,)
        )
        file_path = os.path.join(self.results_directory, server_type, segments_file_name)
        with open(file_path, "r") as f:
            content_lines = [x.strip() for x in f.read().strip().split("\n")]
        to_return = []
        for line in content_lines:
            url_segment, segment_count = line.split("\t")
            to_return.append((url_segment, int(segment_count)))
        if do_sort:
            logger.debug(
                "Now sorting URL segments for server type %s. Total segments count is %s."
                % (server_type, len(to_return))
            )
            to_return = sorted(to_return, key=lambda x: x[1], reverse=True)
        if filter_coerced:
            to_return = filter(lambda x: not self.COERCED_REGEX.findall(x[0]), to_return)
        return to_return

    # Properties

    @property
    def results_directory(self):
        """
        Get the directory path where the Common Crawl results to parse reside.
        :return: the directory path where the Common Crawl results to parse reside.
        """
        return self._results_directory

    # Representation and Comparison

    def __repr__(self):
        return "<%s - %s>" % (self.__class__.__name__, self.results_directory)
