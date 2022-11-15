import logging
import abc
import requests
import bs4
import re

from typing import List, Union
from dataclasses import dataclass
from ugolino.feeditem import FeedItem, Url

logger = logging.Logger(__name__)


@dataclass
class Conference(FeedItem):
    name: str
    description: str
    location: str
    date: str
    link: Union[Url, None]
    source: str

    def __init__(
        self,
        name: str,
        description: str,
        location: str,
        date: str,
        link: Url,
        source: str,
    ) -> "Conference":
        self.name = re.sub("\s+", " ", name.strip().replace("\n", " "))
        self.description = description.strip()
        self.location = location.strip()
        self.date = date.strip()
        self.link = link.strip() if link else link
        if link:
            self.link = Url(link.strip())
        else:
            logger.warn("%s is missing link", self.name)
            self.link = None
        self.source = source.strip()

    def __eq__(self, conf: "Conference"):
        if self.link and conf.link:
            if self.link == conf.link:
                return True
        if self.name == conf.name:
            return True
        return False

    def __hash___(self):
        return 1


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

    def fetch_and_parse(self, url: str, fmt: str = "html.parser") -> bs4.BeautifulSoup:
        content = self.fetch(url)
        # with open("temp", "r") as f:
        #     content = f.read()
        return bs4.BeautifulSoup(content, fmt)
