from typing import List
from ugolino.digests import Digest
from ugolino import Conference, Seminar

from feedgen.feed import FeedGenerator


class RSSDigest(Digest):
    def setup(self, title: str):
        self.title = title
        self.generator = FeedGenerator()
        self.generator.language("en")
        self.generator.title(f"astro-feed-{self.title.lower()}")
        self.generator.link(
            href="https://github.com/astro-grou-bristol/astro-feeds", rel="self"
        )
        self.generator.description(
            f"Astrophysics and astronomy: {self.title}, aggregated from different sources."
        )

    def drain(self) -> str:
        rssfeed = self.generator.rss_str(pretty=True)
        return rssfeed.decode()

    def conference(self, conf: Conference):
        entry = self.generator.add_entry()
        entry.title(f"{conf.format_date()}: {conf.name}")
        if conf.link:
            entry.source(url=conf.link.text, title="Link to page")
        entry.description(f"{conf.location}")
        entry.content(conf.description)

    def seminar(self, sem: Seminar):
        entry = self.generator.add_entry()
        entry.title(f"{sem.format_date()}: {sem.speaker} - {sem.title}")
        if sem.link:
            entry.source(url=sem.source, title="Link to page")
            entry.link(href=sem.link.text, rel="self")
        entry.description(f"{sem.location}")
        entry.content(sem.description)
        entry.author(author={"name": sem.speaker})
