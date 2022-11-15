from typing import List
from ugolino.digests import Digest
from ugolino import Conference

from feedgen.feed import FeedGenerator

class RSSDigest(Digest):
    def setup(self):
        self.generator = FeedGenerator()
        self.generator.language("en")
        self.generator.title("astro-feed")
        self.generator.link(href="todo", rel="self")
        self.generator.description("todo")

    def drain(self) -> str:
        rssfeed  = self.generator.rss_str(pretty=True)
        return rssfeed.decode()

    def conference(self, conf: Conference):
        entry = self.generator.add_entry()
        entry.title(f"{conf.date}: {conf.name}")
        if conf.link:
            entry.link(href=conf.link.text, rel="alternate")
        entry.link(href=conf.source, rel="related")
        entry.description(f"{conf.location}")
        entry.content(conf.description)