


import logging
import re
import bs4

from datetime import datetime
from typing import List, Tuple
from ugolino import Conference, ConferenceFeed
import ugolino.utils as utils

logger = logging.Logger(__name__)


class AthenaFeed(ConferenceFeed):
    ROOT_URL = "https://www.the-athena-x-ray-observatory.eu/en/node/394"

    def scrape_conference(self, item: bs4.BeautifulSoup) -> Conference:
        info = item.find("a")
        title = info.text
        link = info.attrs["href"]

        descr = item.find("p")
        description, date_info = descr.text.split(",")[-2:]
        location = description.strip()
        date = self.parse_date(date_info.strip())
        return Conference(title, description, location, date, link, self.ROOT_URL)
    
    def parse_date(self, date: str) -> datetime:
        matches = re.match(r"(\d+).?(\d+) (\w+) (\d+)", date)
        if matches:
            day, _, month, year = matches.groups()
            s_date = f"{year}/{month[:3]}/{day}"
            d = utils.try_parse(s_date, ("%Y/%b/%d",))
            if d:
                return d
        # some of them are several months, so 
        # we'll just guess the year as current year + 1
        matches = re.match(r"(\d+) (\w+)", date)
        if matches:
            day, month = matches.groups()
            year = datetime.now().year + 1
            s_date = f"{year}/{month[:3]}/{day}"
            d = utils.try_parse(s_date, ("%Y/%b/%d",))
            if d:
                return d
        logger.error("Failed to parse date: %s", date)
        raise "Could not parse date."


    def scrape(self) -> List[Conference]:
        soup = self.fetch_and_parse(self.ROOT_URL)
        return [self.scrape_conference(i) for i in soup.find_all("li", class_="panel-body")]

