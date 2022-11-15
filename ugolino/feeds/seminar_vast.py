import re
import logging
import bs4

from urllib.parse import unquote

from datetime import datetime

from typing import List, Tuple
from ugolino import SeminarFeed, Seminar
import ugolino.utils as utils

logger = logging.Logger(__name__)


class VASTFeed(SeminarFeed):
    ROOT_URL = "https://vast-seminars.github.io/"

    def parse_date_and_title(self, info: str) -> Tuple[datetime, str]:
        matches = re.match(r"(\w+) (\d+), (\d+): (.+)", info)
        month, day, year, title = matches.groups()
        date = f"{year}/{month}/{day}"
        d = utils.try_parse(date, ("%Y/%b/%d", "%Y/%B/%d"))
        if d:
            return d, title
        logger.error("Failed to parse date: %s", date)
        return None, title

    def parse_seminars(self, info: bs4.element.Tag) -> List[Seminar]:
        title_info = unquote(info.h3.text)
        date, description = self.parse_date_and_title(title_info)

        seminars = []
        for item in info.find_all("li"):
            name, title = re.match(r"([\s\-\w]+): (.+)", item.text).groups()
            seminars.append(
                Seminar(
                    title, name, description, "Zoom", date, self.ROOT_URL, self.ROOT_URL
                )
            )
        return seminars

    def scrape(self) -> List[Seminar]:
        soup = self.fetch_and_parse(self.ROOT_URL)
        # find section with the right header
        header: bs4.element.Tag = next(
            filter(
                lambda t: t.h2 is not None and "upcoming" in t.h2.text.lower(),
                soup.find_all("header", class_="major"),
            )
        )
        if not header:
            raise Exception("Could not find VAST seminar upcoming section.")

        seminars = []
        for i in header.parent.find_all("article"):
            seminars += self.parse_seminars(i)
        return seminars
