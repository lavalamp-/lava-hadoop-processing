lava-hadoop-processing
=======================

This code is written to process the results of data gathered using [Amazon Elastic MapReduce](https://aws.amazon.com/emr/) to aggregate URL path segments by web server types. The Hadoop code to gather this data can be found in the [LavaHadoopCrawlAnalysis](https://github.com/lavalamp-/LavaHadoopCrawlAnalysis) GitHub repository.

To get anywhere with this code, you will need all of the Hadoop result files (ex: `part-00000`, `part-00001`, etc) that are generated using the LavaHadoopCrawlAnalysis code. Once the Hadoop jobs have completed, these data files will be stored in the S3 bucket that you configured via the `fileOutputPath` variable in the LavaHadoopCrawlAnalysis code. Use the [AWS command line tools](https://aws.amazon.com/cli/) to copy all of the result files to your local machine using the following command:

```
aws s3 sync <s3 URL> .
```

Once the results of your Hadoop jobs are pulled down locally, you can do one of three things with this tool:

* Process the result files into lists of URL segments and their associated numbers of occurences (`process-results`)
* Process the URL segment & occurence files into content discovery hit lists separated out by web server type (`generate-hit-lists`)
* Both of the above in succession (`do-all`)

All functionality is invoked using the `run.py` file (ex: `python run.py process-results`).

The code is fully documented and uses `argparse`, so command line help should go a long way with getting things going for you.

Command help for `process-results` is below:

```
usage: run.py process-results [-h] --results-directory <results directory>
                              [--ignore-threshold <ignore threshold>]
                              [--report-interval <report interval>]
                              [--output-directory <output directory>]

optional arguments:
  -h, --help            show this help message and exit
  --results-directory <results directory>, -r <results directory>
                        The local file path to the directory that contains the
                        Hadoop results file (ex: part-00000, part-00001, etc).
  --ignore-threshold <ignore threshold>, -i <ignore threshold>
                        The prevalence threshold to ignore identified URL
                        segments upon. This means that with a threshold of 10,
                        any URL segments that were seen less than 10 times
                        will not be included in the resulting URL segment
                        files.
  --report-interval <report interval>, -v <report interval>
                        The interval upon which the Hadoop results processing
                        should echo progress to the console.
  --output-directory <output directory>, -o <output directory>
                        The root directory where the results of parsing Hadoop
                        results will be stored.
```

Command help for `generate-hit-lists` is below:

```
usage: run.py generate-hit-lists [-h]
                                 [--processed-directory <processed directory>]
                                 [--thresholds <50 75 90 95 99 99.7 99.9> [<50 75 90 95 99 99.7 99.9> ...]]
                                 [--file-name <hit_list_>]

optional arguments:
  -h, --help            show this help message and exit
  --processed-directory <processed directory>, -p <processed directory>
                        The directory where the results of processing Hadoop
                        results reside.
  --thresholds <50 75 90 95 99 99.7 99.9> [<50 75 90 95 99 99.7 99.9> ...], -t <50 75 90 95 99 99.7 99.9> [<50 75 90 95 99 99.7 99.9> ...]
                        A list of integers and floats representing the
                        percentages of hit list coverages to generate hit
                        lists for.
  --file-name <hit_list_>, -f <hit_list_>
                        The start of the file name to write hit list files out
                        to.
```

Command help for `do-all` is below:

```
usage: run.py do-all [-h] --results-directory <results directory>
                     [--ignore-threshold <ignore threshold>]
                     [--report-interval <report interval>]
                     [--output-directory <output directory>]
                     [--thresholds <50 75 90 95 99 99.7 99.9> [<50 75 90 95 99 99.7 99.9> ...]]
                     [--file-name <hit_list_>]

optional arguments:
  -h, --help            show this help message and exit
  --results-directory <results directory>, -r <results directory>
                        The local file path to the directory that contains the
                        Hadoop results file (ex: part-00000, part-00001, etc).
  --ignore-threshold <ignore threshold>, -i <ignore threshold>
                        The prevalence threshold to ignore identified URL
                        segments upon. This means that with a threshold of 10,
                        any URL segments that were seen less than 10 times
                        will not be included in the resulting URL segment
                        files.
  --report-interval <report interval>, -v <report interval>
                        The interval upon which the Hadoop results processing
                        should echo progress to the console.
  --output-directory <output directory>, -o <output directory>
                        The root directory where the results of parsing Hadoop
                        results will be stored.
  --thresholds <50 75 90 95 99 99.7 99.9> [<50 75 90 95 99 99.7 99.9> ...], -t <50 75 90 95 99 99.7 99.9> [<50 75 90 95 99 99.7 99.9> ...]
                        A list of integers and floats representing the
                        percentages of hit list coverages to generate hit
                        lists for.
  --file-name <hit_list_>, -f <hit_list_>
                        The start of the file name to write hit list files out
                        to.
```

If you're only interested in the content discovery hit lists that have been generated using this project and [LavaHadoopCrawlAnalysis](https://github.com/lavalamp-/LavaHadoopCrawlAnalysis), head on over to the [content-discovery-hit-lists](https://github.com/lavalamp-/content-discovery-hit-lists) repository.