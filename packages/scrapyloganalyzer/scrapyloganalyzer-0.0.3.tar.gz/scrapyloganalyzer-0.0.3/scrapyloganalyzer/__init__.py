import ast
import datetime
import os
import re
from collections import defaultdict

from logparser import parse
from logparser.common import DATETIME_PATTERN, Common

# Kingfisher Collect logs an INFO message starting with "Spider arguments:".
SPIDER_ARGUMENTS_SEARCH_STRING = " INFO: Spider arguments: "

MAXIMUM_TIMEDELTA = 3

# Hotfix: https://github.com/my8100/logparser/pull/19
Common.SIGTERM_PATTERN = re.compile(r"^%s[ ].+?:[ ](Received[ ]SIG(?:BREAK|INT|TERM)([ ]twice)?)," % DATETIME_PATTERN)  # noqa: UP031


class ScrapyLogFile:
    """A representation of a Scrapy log file."""

    @classmethod
    def find(cls, logs_directory, source_id, data_version):
        """
        Find and return the first matching log file for the given crawl.

        :param str logs_directory: Kingfisher Collect's project directory within Scrapyd's logs_dir directory
        :param str source_id: the spider's name
        :param datetime.datetime data_version: the crawl directory's name, parsed as a datetime
        """
        source_directory = os.path.join(logs_directory, source_id)
        if os.path.isdir(source_directory):
            with os.scandir(source_directory) as it:
                for entry in it:
                    if entry.name.endswith(".log"):
                        scrapy_log_file = ScrapyLogFile(entry.path)
                        if scrapy_log_file.match(data_version):
                            return scrapy_log_file
        return None

    def __init__(self, name: str, text: str = "") -> None:
        """
        :param name: the full path to the log file
        :param text: the text content of the log file
        """
        self.name = name
        self.text = text

        self._logparser = None
        self._item_counts = None
        self._spider_arguments = None

    def delete(self):
        """Delete the log file and any log summary ending in ``.stats``."""
        if self.name:
            if os.path.isfile(self.name):
                os.remove(self.name)
            summary = f"{self.name}.stats"
            if os.path.isfile(summary):
                os.remove(summary)

    # Logparser processing

    @property
    def logparser(self) -> dict:
        """Return the output of `logparser <https://pypi.org/project/logparser/>`__."""
        if self._logparser is None:
            # `taillines=0` sets the 'tail' key to all lines, so we set it to 1.
            self._logparser = parse(self.read(), headlines=0, taillines=1)

        return self._logparser

    def match(self, data_version) -> bool:
        """
        Return whether the crawl directory's name, parsed as a datetime, is less than 3 seconds after the log file's
        start time.
        """
        return 0 <= data_version.timestamp() - self.crawl_time.timestamp() < MAXIMUM_TIMEDELTA

    @property
    def crawl_time(self) -> datetime.datetime:
        """
        Return the ``crawl_time`` spider argument if set, or the ``start_time`` crawl statistic otherwise. If neither
        is logged, return the time of the first log message.
        """
        crawl_time = self.spider_arguments.get("crawl_time")
        if crawl_time:
            return datetime.datetime.strptime(crawl_time, "%Y-%m-%dT%H:%M:%S")
        if "start_time" in self.logparser["crawler_stats"]:
            return eval(self.logparser["crawler_stats"]["start_time"]).replace(microsecond=0)  # noqa: S307
        return datetime.datetime.fromtimestamp(self.logparser["first_log_timestamp"])

    def is_finished(self) -> bool:
        """
        Return whether the log file contains a "Spider closed (finished)" log message or a ``finish_reason`` crawl
        statistic set to "finished".
        """
        # See https://kingfisher-collect.readthedocs.io/en/latest/logs.html#check-the-reason-for-closing-the-spider
        # logparser's `finish_reason` is "N/A" for an unclean shutdown, because crawl statistics aren't logged.
        return self.logparser["finish_reason"] == "finished"

    # Line-by-line processing

    @property
    def item_counts(self) -> dict:
        """Return the number of each type of item, according to the log file."""
        if self._item_counts is None:
            self._process_line_by_line()

        return self._item_counts

    @property
    def spider_arguments(self) -> dict:
        """Return the spider's arguments."""
        if self._spider_arguments is None:
            self._process_line_by_line()

        return self._spider_arguments

    def is_complete(self) -> bool:
        """Return whether the crawl collected a subset of the dataset, according to the log file."""
        # See https://kingfisher-collect.readthedocs.io/en/latest/spiders.html#spider-arguments
        return not any(
            self.spider_arguments.get(arg)
            for arg in (
                "from_date",
                "until_date",
                "portal",
                "publisher",
                "system",
                "sample",
                "path",
                "qs:",
            )
        )

    def read(self):
        """Return the text content of the log file."""
        if self.text:
            return self.text
        with open(self.name) as f:
            return f.read()

    def __iter__(self):
        """Yield each line of the log file."""
        if self.text:
            for line in self.text.splitlines(keepends=True):
                yield line
        else:
            with open(self.name) as f:
                for line in f:
                    yield line

    def _process_line_by_line(self) -> None:
        self._item_counts = defaultdict(int)
        self._spider_arguments = {}

        buf = []
        for line in self:
            if buf or line.startswith("{"):
                buf.append(line.rstrip())
            if buf and buf[-1].endswith("}"):
                try:
                    # Scrapy logs items as dicts. FileError items, representing retrieval errors, are identified by
                    # an 'errors' key. FileError items use only simple types, so `ast.literal_eval` can be used.
                    item = ast.literal_eval("".join(buf))
                    if "errors" in item:
                        self._item_counts["FileError"] += 1
                    elif "number" in item:
                        self._item_counts["FileItem"] += 1
                    elif "data_type" in item:
                        self._item_counts["File"] += 1
                except ValueError:
                    # Scrapy dumps stats as a dict, which uses `datetime.datetime` types that can't be parsed with
                    # `ast.literal_eval`.
                    pass
                buf = []

            index = line.find(SPIDER_ARGUMENTS_SEARCH_STRING)
            if index > -1:
                # `eval` is used, because the string can contain `datetime.date` and is written by trusted code in
                # Kingfisher Collect. Otherwise, we can modify the string so that `ast.literal_eval` can be used.
                self._spider_arguments = eval(line[index + len(SPIDER_ARGUMENTS_SEARCH_STRING) :])  # noqa: S307

    # Mixed processing

    @property
    def error_rate(self) -> float:
        """
        Return an estimated lower bound of the true error rate.

        Kingfisher Collect is expected to yield at most one FileError item per request leading to a File item, so the
        true error rate can only be less than this estimated lower bound if Kingfisher Collect breaks this expectation.
        On the other hand, the true error rate can easily be higher than the estimated lower bound; for example:

        -  If the spider crawls 10 URLs, each returning 99 URLs, each returning OCDS data, and the requests for 5 of
           the 10 fail, then the estimated lower bound is 5 / 500 (1%), though the true error rate is 50%.
        -  Similarly if the spider crawls 10 archive files, each containing 99 OCDS files, or 10 JSON files each
           containing 99 release packages.
        """
        error_count = self.item_counts["FileError"] + self.logparser["crawler_stats"].get("invalid_json_count", 0)
        return error_count / (self.item_counts["File"] + self.item_counts["FileItem"] + error_count)
