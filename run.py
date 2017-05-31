# -*- coding: utf-8 -*-
from __future__ import absolute_import

import argparse
import logging
from datetime import datetime
import os
import shutil

from lib import CCResultParser, LavaUIFactory, ConfigManager, LavaLogFormatter, HitListParser

logger = logging.getLogger(__name__)


def configure_logging(log_level):
    """
    Configure logging.
    :param log_level: The level to configure logging at.
    :return: None
    """
    lvl = None
    if log_level.upper() == "INFO":
        lvl = logging.INFO
    elif log_level.upper() == "WARNING":
        lvl = logging.WARNING
    elif log_level.upper() == "ERROR":
        lvl = logging.ERROR
    elif log_level.upper() == "CRITICAL":
        lvl = logging.CRITICAL
    elif log_level.upper() == "DEBUG":
        lvl = logging.DEBUG
    if not lvl:
        raise ValueError("%s is not a valid log level." % log_level)
    logger.setLevel(lvl)
    formatter = LavaLogFormatter()
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    ConfigManager.LOGGING_LEVEL = lvl


def do_all(input_args):
    """
    Process the contents of the referenced Hadoop results and then generate hit lists based on the
    processed data.
    :param input_args: Arguments retrieved through parsing command line input.
    :return: None
    """
    logger.info("Now processing Hadoop data and then generating hit lists.")
    input_args.processed_directory = input_args.output_directory
    do_process_hadoop_results(input_args)
    do_generate_hit_lists(input_args)
    logger.info("Hadoop data processed and hit lists generated!")


def do_generate_hit_lists(input_args):
    """
    Process the contents of the cleaned URL segments and counts processed from Hadoop results into hit lists
    by server types.
    :param input_args: Arguments retrieved through parsing command line input.
    :return: None
    """
    logger.info(
        "Now generating hit lists for all server types found in directory %s. Thresholds will be %s. "
        "File names will start with %s."
        % (
            input_args.processed_directory,
            ", ".join([str(x) for x in input_args.thresholds]),
            input_args.hit_list_preamble,
        )
    )
    hit_list_parser = HitListParser(results_directory=input_args.processed_directory)
    logger.info("Now starting hit list generation.")
    hit_list_parser.generate_hit_lists_for_all_servers(
        thresholds=input_args.thresholds,
        hit_list_preamble=input_args.hit_list_preamble,
    )
    logger.info(
        "Hit lists generated for all server types found in directory %s."
        % (input_args.processed_directory,)
    )


def do_process_hadoop_results(input_args):
    """
    Process the contents of the referenced Hadoop results.
    :param input_args: Arguments retrieved through parsing command line input.
    :return: None
    """
    logger.info(
        "Now processing Hadoop results stored in directory %s. Ignore threshold is %s, and report interval is %s. "
        "Parsed results will be stored at %s."
        % (
            input_args.results_directory,
            input_args.ignore_threshold,
            input_args.report_interval,
            input_args.output_directory,
        )
    )
    if os.path.isdir(input_args.output_directory):
        logger.info("Output directory at %s already exists. Delete it?\n")
        response = raw_input("Delete directory %s? [Y/n]: " % input_args.output_directory)
        if response in ["", "y", "Y"]:
            shutil.rmtree(input_args.output_directory)
            print("")
            logger.info(
                "Directory at %s successfully deleted!"
                % (input_args.output_directory,)
            )
        else:
            print("")
            logger.info(
                "Not deleting results directory at %s. Please choose a different output directory and try again."
                % (input_args.output_directory,)
            )
            return
    results_parser = CCResultParser(input_args.results_directory)
    logger.info(
        "Now processing the contents of Hadoop results stored in %s. This will take a while."
        % (input_args.results_directory,)
    )
    results_parser.process_files_in_directory(
        ignore_threshold=input_args.ignore_threshold,
        report_interval=input_args.report_interval,
        output_directory=input_args.output_directory,
    )
    logger.info(
        "All Hadoop results stored in %s were successfully processed!"
        % (input_args.results_directory,)
    )


def main():
    """
    Handle the main software invocation.
    :return: None
    """
    print_greeting()
    args = parse_arguments()
    configure_logging(args.log_level)
    start_time = datetime.now()
    logger.info(
        "Script invocation starting at time %s."
        % (start_time.strftime("%m/%d/%Y %H:%M:%S"))
    )
    try:
        args.func(args)
    except KeyboardInterrupt:
        logger.warning("Keyboard interrupt received!")
    end_time = datetime.now()
    elapsed = end_time - start_time
    logger.info(
        "Script completed at time %s. Elapsed time was %s seconds."
        % (end_time.strftime("%m/%d/%Y %H:%M:%S"), elapsed.seconds)
    )


def parse_arguments():
    """
    Parse command line arguments and return them.
    :return: The parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="lava-hadoop-processing - for making sweet content discovery hit lists"
    )
    subparsers = parser.add_subparsers(
        help="<sub-command> --help",
        description="lava-hadoop-processing contains three commands that you can invoke to parse "
                    "the contents of results retrieved through lavalamp's Common Crawl Hadoop code: "
                    "process-results, generate-hit-lists, and process-all.",
    )
    parser.add_argument(
        "--log-level",
        required=False,
        help="The log message level to receive when running the script. Valid "
            "values are DEBUG, INFO, WARNING, ERROR, CRITICAL.",
        action="store",
        dest="log_level",
        metavar="<DEBUG|INFO|WARNING|ERROR|CRITICAL>",
        default="DEBUG",
        type=str
    )
    results_parser = subparsers.add_parser(
        "process-results",
        help="Process the results retrieved via Hadoop from analyzing the contents of the Common Crawl "
             "data to retrieve server heaeders and URL segments.",
    )
    results_parser.add_argument(
        "--results-directory",
        "-r",
        required=True,
        help="The local file path to the directory that contains the Hadoop results file "
             "(ex: part-00000, part-00001, etc).",
        action="store",
        dest="results_directory",
        type=str,
        metavar="<results directory>",
    )
    results_parser.add_argument(
        "--ignore-threshold",
        "-i",
        required=False,
        help="The prevalence threshold to ignore identified URL segments upon. This means "
             "that with a threshold of 10, any URL segments that were seen less than 10 times "
             "will not be included in the resulting URL segment files.",
        action="store",
        dest="ignore_threshold",
        type=int,
        metavar="<ignore threshold>",
        default=ConfigManager.IGNORE_THRESHOLD,
    )
    results_parser.add_argument(
        "--report-interval",
        "-v",
        required=False,
        help="The interval upon which the Hadoop results processing should echo progress to the console.",
        action="store",
        dest="report_interval",
        type=int,
        metavar="<report interval>",
        default=ConfigManager.REPORT_INTERVAL,
    )
    results_parser.add_argument(
        "--output-directory",
        "-o",
        required=False,
        help="The root directory where the results of parsing Hadoop results will be stored.",
        action="store",
        dest="output_directory",
        type=str,
        metavar="<output directory>",
        default=ConfigManager.OUTPUT_DIRECTORY,
    )
    results_parser.set_defaults(func=do_process_hadoop_results)
    hit_list_parser = subparsers.add_parser(
        "generate-hit-lists",
        help="Generate content discovery hit lists based on the parsed results of a Common Crawl Hadoop analysis.",
    )
    hit_list_parser.add_argument(
        "--processed-directory",
        "-p",
        required=False,
        help="The directory where the results of processing Hadoop results reside.",
        action="store",
        dest="processed_directory",
        type=str,
        metavar="<processed directory>",
        default=ConfigManager.OUTPUT_DIRECTORY,
    )
    hit_list_parser.add_argument(
        "--thresholds",
        "-t",
        required=False,
        help="A list of integers and floats representing the percentages of hit list coverages "
             "to generate hit lists for.",
        nargs="+",
        action="store",
        dest="thresholds",
        type=float,
        metavar="<50 75 90 95 99 99.7 99.9>",
        default=ConfigManager.DEFAULT_THRESHOLDS,
    )
    hit_list_parser.add_argument(
        "--file-name",
        "-f",
        required=False,
        help="The start of the file name to write hit list files out to.",
        action="store",
        dest="hit_list_preamble",
        type=str,
        metavar="<hit_list_>",
        default=ConfigManager.HIT_LIST_FILE_PREAMBLE,
    )
    hit_list_parser.set_defaults(func=do_generate_hit_lists)
    do_all_parser = subparsers.add_parser(
        "do-all",
        help="First process the contents of the Hadoop Common Crawl results. Once results have been "
             "processed, use the processed results to generate hit lists for all of the discovered "
             "server types."
    )
    do_all_parser.add_argument(
        "--results-directory",
        "-r",
        required=True,
        help="The local file path to the directory that contains the Hadoop results file "
             "(ex: part-00000, part-00001, etc).",
        action="store",
        dest="results_directory",
        type=str,
        metavar="<results directory>",
    )
    do_all_parser.add_argument(
        "--ignore-threshold",
        "-i",
        required=False,
        help="The prevalence threshold to ignore identified URL segments upon. This means "
             "that with a threshold of 10, any URL segments that were seen less than 10 times "
             "will not be included in the resulting URL segment files.",
        action="store",
        dest="ignore_threshold",
        type=int,
        metavar="<ignore threshold>",
        default=ConfigManager.IGNORE_THRESHOLD,
    )
    do_all_parser.add_argument(
        "--report-interval",
        "-v",
        required=False,
        help="The interval upon which the Hadoop results processing should echo progress to the console.",
        action="store",
        dest="report_interval",
        type=int,
        metavar="<report interval>",
        default=ConfigManager.REPORT_INTERVAL,
    )
    do_all_parser.add_argument(
        "--output-directory",
        "-o",
        required=False,
        help="The root directory where the results of parsing Hadoop results will be stored.",
        action="store",
        dest="output_directory",
        type=str,
        metavar="<output directory>",
        default=ConfigManager.OUTPUT_DIRECTORY,
    )
    do_all_parser.add_argument(
        "--thresholds",
        "-t",
        required=False,
        help="A list of integers and floats representing the percentages of hit list coverages "
             "to generate hit lists for.",
        nargs="+",
        action="store",
        dest="thresholds",
        type=float,
        metavar="<50 75 90 95 99 99.7 99.9>",
        default=ConfigManager.DEFAULT_THRESHOLDS,
    )
    do_all_parser.add_argument(
        "--file-name",
        "-f",
        required=False,
        help="The start of the file name to write hit list files out to.",
        action="store",
        dest="hit_list_preamble",
        type=str,
        metavar="<hit_list_>",
        default=ConfigManager.HIT_LIST_FILE_PREAMBLE,
    )
    do_all_parser.set_defaults(func=do_all)
    return parser.parse_args()


def print_greeting():
    """
    Print a colorized splash screen to welcome all the peeps.
    :return: None
    """
    print(LavaUIFactory.get_colorized_lavalamp_splash())
    print("                              /***************************\                                   ")
    print("-= Presents \033[31mlava-hadoop-processing\033[0m, for making sweet content discovery lists =-")
    print("                              \***************************/                                   ")
    print("")


if __name__ == "__main__":
    main()
