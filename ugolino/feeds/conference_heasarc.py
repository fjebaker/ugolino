import logging
import re
import bs4
from datetime import datetime, date

from typing import List
from ugolino import ConferenceFeed, Conference
import ugolino.utils as utils

logger = logging.Logger(__name__)


class HEASARCFeed(ConferenceFeed):
    ROOT_URL = "https://heasarc.gsfc.nasa.gov/docs/heasarc/meetings.html"

    def conference_finder(self, soup: bs4.BeautifulSoup):
        # their website is a mess so have to go through the tags one by one
        # since nesting is meaningless
        for tag in soup.find_all(lambda t: t.name.lower() in ["dd", "dt"]):
            if tag.a is not None:
                if "name" in tag.a.attrs and re.match(r"M\d+", tag.a.attrs["name"]):
                    # this tag is the first thing that marks a conference descriptioniption
                    yield tag

    def parse_date(self, date: str) -> datetime:
        matches = re.match(r"(\d\d\d\d) (\w+) (\d+)", date)
        year, month, day = matches.groups()
        date = f"{year}/{month}/{day}"
        d = utils.try_parse(date, ("%Y/%b/%d", "%Y/%B/%d"))
        if d:
            return d
        logger.error("Failed to parse date: %s", date)
        return None

    def parse_conference(self, info: bs4.element.Tag) -> Conference:
        title_tag = info.find(lambda t: t.name == "a" and t.b is not None)
        url = title_tag.attrs.get("href", "")
        title = title_tag.b.text
        date = None
        location = None
        description = None

        for tag in info.find_all("dd"):
            # get date
            matches = re.findall("Meeting Dates: (.+)", tag.text)
            if matches:
                date = self.parse_date(matches[0])
                continue
            # location
            matches = re.findall("Meeting Location: (.+)", tag.text)
            if matches:
                location = matches[0]
                continue
            # description
            description = tag.text

        return Conference(title, description, location, date, url, self.ROOT_URL)

    def scrape(self) -> List[Conference]:
        soup = self.fetch_and_parse(self.ROOT_URL)
        return [self.parse_conference(i) for i in self.conference_finder(soup)]
