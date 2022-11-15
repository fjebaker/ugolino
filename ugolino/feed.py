import logging
import requests
import bs4
import abc

from typing import List
from ugolino.feeditem import FeedItem

logger = logging.Logger(__name__)


class AbstractFeed(abc.ABC):
    # want to look as human as possible, so will have all scrapers use the same requests instance
    session = requests.Session()

    @abc.abstractmethod
    def scrape(self) -> List[FeedItem]:
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
        # with open("temp", "w") as f:
        #     f.write(content)
        # with open("temp", "r") as f:
        #     content = f.read()
        return bs4.BeautifulSoup(content, fmt)
