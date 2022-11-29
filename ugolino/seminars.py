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
class Seminar(FeedItem):
    title: str
    speaker: str
    description: str
    location: str
    date: datetime
    link: Union[Url, None]
    source: str

    def __init__(
        self,
        title: str,
        speaker: str,
        description: str,
        location: str,
        date: datetime,
        link: Url,
        source: str,
    ) -> "Seminar":
        self.title = self.clean(title)
        self.speaker = self.clean(speaker)
        self.description = self.clean(description)
        self.location = self.clean(location)

        if type(date) is not datetime:
            raise Exception(f"Date for {title} is not datetime (is {type(date)}).")
        self.date = date

        if link:
            self.link = Url(link.strip())
        else:
            logger.warn("%s is missing link", self.title)
            self.link = None
        self.source = source.strip()

    def __eq__(self, other: "Seminar"):
        if self.link and other.link:
            if self.link == other.link and self.source != other.source:
                return True
        if (
            self.title.lower() == other.title.lower()
            and self.speaker.lower() == other.speaker.lower()
        ):
            return True
        return False


class SeminarFeed(AbstractFeed):
    @abc.abstractmethod
    def scrape(self) -> List[Seminar]:
        ...
