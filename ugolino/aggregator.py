from typing import List
from ugolino import Conference
from ugolino.feeds import conference_feeds
from ugolino.digests import MarkdownDigest


class Aggregator:
    def __init__(self):
        self.conferences: List[Conference] = []
        self.markdown = MarkdownDigest(self)

    def filter_new(self):
        self._filter_new(self.conferences)

    def fetch_all(self):
        self._get_conferences()
        # ... todo: others

    def _filter_new(self, items: List):
        ...

    def _get_conferences(self):
        conferences = []
        for scraper in conference_feeds:
            cs = scraper().scrape()
            conferences += cs
        self.conferences = conferences
