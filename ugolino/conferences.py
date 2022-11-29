import logging
import abc
import re

from datetime import datetime
from typing import List, Union
from dataclasses import dataclass
from ugolino import FeedItem, AbstractFeed
from ugolino.utils import Url

logger = logging.Logger(__name__)


@dataclass
class Conference(FeedItem):
    name: str
    description: str
    location: str
    date: datetime
    link: Union[Url, None]
    source: str

    def __init__(
        self,
        name: str,
        description: str,
        location: str,
        date: datetime,
        link: Url,
        source: str,
    ) -> "Conference":
        self.name = re.sub("\s+", " ", name.strip().replace("\n", " "))
        self.description = description.strip()
        self.location = location.strip()

        if type(date) is not datetime:
            raise Exception(f"Date for {name} is not datetime (is {type(date)}).")
        self.date = date

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
        if self.name.lower() == conf.name.lower():
            return True
        return False


class ConferenceFeed(AbstractFeed):
    @abc.abstractmethod
    def scrape(self) -> List[Conference]:
        ...
