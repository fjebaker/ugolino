import re
import logging
import bs4

from urllib.parse import unquote

from datetime import datetime

from typing import List, Tuple, Iterator
from ugolino import SeminarFeed, Seminar
import ugolino.utils as utils

logger = logging.Logger(__name__)


class IAUAIIFeed(SeminarFeed):
    ROOT_URL = "https://sites.google.com/view/iau-iaa-seminar/schedule?authuser=0"
    SOURCE_URL = "https://sites.google.com/view/iau-iaa-seminar"

    def get_upcoming(self, header: bs4.element.Tag) -> Iterator[bs4.element.Tag]:
        for item in header.parent.find_all("section"):
            if "past seminars" in item.text.lower():
                break
            # use bullet point as a pivot
            for bullet in item.find_all("ul"):
                yield bullet.parent

    def parse_date(self, info: str) -> datetime:
        matches = re.match(r"(\d+) (\w+) (\d+) \/ (\d+):(\d+) \((\w+)\)", info)
        day, month, year, hour, minute, tz = matches.groups()
        date = f"{year}/{month[0:3]}/{day} {hour}:{minute}/{tz}"
        d = utils.try_parse(date, ("%Y/%b/%d %H:%M/%Z",))
        if d:
            return d
        logger.error("Failed to parse date: %s", date)
        return None

    def parse_seminar(self, info: bs4.element.Tag) -> Seminar:
        date = self.parse_date(info.find("ul").text)
        description = ""
        itt = (i for i in info.find_all("p"))

        # discard date
        _ = next(itt)
        # first one is always author
        author, location = re.match(
            r"([\w\-\,\.\s]+) \(([\w\s\,\-]+)\)", next(itt).text
        ).groups()
        title = next(itt).text
        description = next(itt).text

        return Seminar(
            title,
            author,
            description,
            "Zoom ({})".format(location),
            date,
            self.SOURCE_URL,
            self.ROOT_URL,
        )

    def scrape(self) -> List[Seminar]:
        soup = self.fetch_and_parse(self.ROOT_URL)

        # find where current seminars start and stop
        header = soup.find(
            lambda t: t.name == "section" and "upcoming" in t.text.lower()
        )

        return [self.parse_seminar(i) for i in self.get_upcoming(header)]
