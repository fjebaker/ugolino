from typing import List
from ugolino import Conference
from ugolino.feeds import conference_feeds
from ugolino.digests import MarkdownDigest, RSSDigest


class Aggregator:
    def __init__(self):
        self.conferences: List[Conference] = []
        self.markdown = MarkdownDigest(self)
        self.rss = RSSDigest(self)

    def filter_new(self):
        self._filter_new(self.conferences)

    def fetch_all(self):
        self._get_conferences()
        # ... todo: others

    def sort(self):
        self.conferences = sorted(self.conferences, key=lambda c: c.date)
    
    def _filter_new(self, items: List):
        ...

    def filter_unique(self):
        self.conferences = self.unique_keep_order(self.conferences)

    def _get_conferences(self):
        conferences = []
        for scraper in conference_feeds:
            cs = scraper().scrape()
            conferences += cs
        self.conferences = conferences

    def unique_keep_order(self, items: List) -> List:
        uniques = []
        for i in items:
            for j in uniques:
                if i == j:
                    print("Duplicate: {}".format(i.name))
                    continue
            uniques.append(i)
        return uniques
