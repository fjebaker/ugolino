from typing import List
from ugolino.digests import Digest
from ugolino import Conference

from feedgen.feed import FeedGenerator


class RSSDigest(Digest):
    def setup(self):
        self.generator = FeedGenerator()
        self.generator.language("en")
        self.generator.title("astro-feed")
        self.generator.link(
            href="https://github.com/astro-grou-bristol/astro-feeds", rel="self"
        )
        self.generator.description(
            "Astrophysics and astronomy conferences, aggregated from different sources."
        )

    def drain(self) -> str:
        rssfeed = self.generator.rss_str(pretty=True)
        return rssfeed.decode()

    def conference(self, conf: Conference):
        entry = self.generator.add_entry()
        entry.title(f"{conf.format_date()}: {conf.name}")
        if conf.link:
            entry.link(href=conf.link.text, rel="related")
        entry.link(href=conf.source, rel="via")
        entry.description(f"{conf.location}")
        entry.content(conf.description)
