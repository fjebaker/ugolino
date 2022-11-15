import logging
import abc
import requests
import bs4
import re

from typing import List
from dataclasses import dataclass
from ugolino.feeditem import FeedItem

logger = logging.Logger(__name__)


@dataclass
class Conference(FeedItem):
    name: str
    description: str
    location: str
    date: str
    link: str
    source: str

    def __init__(
        self,
        name: str,
        description: str,
        location: str,
        date: str,
        link: str,
        source: str,
    ) -> "Conference":
        self.name = re.sub("\s+", " ", name.strip().replace("\n", " "))
        self.description = description.strip()
        self.location = location.strip()
        self.date = date.strip()
        self.link = link.strip() if link else link
        if link:
            self.link = link.strip()
        else:
            logger.warn("%s is missing link", self.name)
            self.link = ""
        self.source = source.strip()


class ConferenceFeed(abc.ABC):
    # want to look as human as possible, so will have all scrapers use the same requests instance
    session = requests.Session()

    @abc.abstractmethod
    def scrape(self) -> List[Conference]:
        ...

    def fetch(self, url: str) -> str:
        resp = self.session.get(url)
        if 200 <= resp.status_code < 300:
            logger.info("Request to %s returned with status %d", url, resp.status_code)
            return resp.content.decode()
        else:
            logger.error("Request to %s failed: %s", url, resp)
            raise resp

    def fetch_and_parse(self, url: str) -> bs4.BeautifulSoup:
        content = self.fetch(url)
        return bs4.BeautifulSoup(content, "html.parser")
