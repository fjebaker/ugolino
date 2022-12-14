import logging
import re
import bs4

from datetime import datetime
from typing import List, Tuple
from ugolino import Conference, ConferenceFeed
import ugolino.utils as utils

logger = logging.Logger(__name__)


class CACDFeed(ConferenceFeed):
    ROOT_URL = "https://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/meetings/rssFeed"

    def sub_escapes(self, text: str) -> str:
        return text.replace("&lt;", "<").replace("&gt;", ">")

    def parse_date(self, date: str) -> datetime:
        matches = re.match(r"(\w+) (\d+), (\w+) (\d+)", date)
        _, day, month, year = matches.groups()
        date = f"{year}/{month}/{day}"
        d = utils.try_parse(date, ("%Y/%B/%d",))
        if d:
            return d
        logger.error("Failed to parse date: %s", date)
        return None

    def parse_description(self, descr: str) -> Tuple[str, str]:
        soup = bs4.BeautifulSoup(self.sub_escapes(descr), "xml")
        itt = (i for i in soup.find_all("TD"))

        date = ""
        location = ""
        for i in itt:
            if i.text == "Date":
                date = self.parse_date(next(itt).text)
            elif i.text == "Location":
                location = next(itt).text

        return date, location

    def parse_conference(self, info: bs4.element.Tag) -> Conference:
        title = info.title.text
        link = info.link.text
        source = info.guid.text

        date, location = self.parse_description(info.description.text)
        description = "No information available."

        return Conference(title, description, location, date, link, source)

    def scrape(self) -> List[Conference]:
        soup = self.fetch_and_parse(self.ROOT_URL, fmt="xml")
        return [self.parse_conference(i) for i in soup.find_all("item")]
