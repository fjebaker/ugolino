from typing import List
from ugolino import Conference, FeedItem
from ugolino.feeds import conference_feeds, seminar_feeds
from ugolino.digests import MarkdownDigest, RSSDigest


class Aggregator:
    def __init__(self):
        self.conferences: List[Conference] = []
        self.markdown = MarkdownDigest(self)
        self.rss = RSSDigest(self)

    def filter_new(self):
        self._filter_new(self.conferences)

    def fetch_conferences(self):
        conferences = []
        for scraper in conference_feeds:
            cs = scraper().scrape()
            conferences += cs
        self.conferences = conferences

    def fetch_seminars(self):
        seminars = []
        for scraper in seminar_feeds:
            ss = scraper().scrape()
            seminars += ss
        self.seminars = seminars

    def fetch(self, name: str):
        if name == "iauiaa":
            self.seminars = seminar_feeds[1]().scrape()
        else:
            raise Exception("Unknown feed {}".format(name))

    def fetch_all(self):
        self.fetch_conferences()
        self.fetch_seminars()

    def sort(self):
        self.conferences = sorted(self.conferences, key=lambda c: c.date)
        self.seminars = sorted(self.seminars, key=lambda c: c.date)

    def _filter_new(self, items: List):
        ...

    def filter_unique(self):
        self.conferences = self.unique_keep_order(self.conferences)
        self.seminars = self.unique_keep_order(self.seminars)

    def unique_keep_order(self, items: List[FeedItem]) -> List:
        uniques = []
        for i in items:
            for j in uniques:
                if i == j:
                    print("Duplicate: {}".format(i.name))
                    i.merge_with(j)
                    break
            else:
                uniques.append(i)
        return uniques
