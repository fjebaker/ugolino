from typing import List
from ugolino import Conference
from ugolino.feeds import conference_feeds

def sanitize(s: str) -> str:
    return s.replace(":", "")

def create_github_header_anchor(title, header_title):
    return '[{}](#{})'.format(title, sanitize(header_title.strip().replace(' ', '-')))

class Aggregator:

    def __init__(self):
        self.conferences : List[Conference] = []

    def create_digest(self, _type: str) -> str:
        if _type == "markdown":
            s = [conf.to_markdown() for conf in self.conferences]
            confs = "\n\n".join(s)
            return confs
        else:
            raise f"Unknown digest {_type}"

    def create_toc(self) -> str:
        toc = "## Table of Contents\n"
        for conf in self.conferences:
            i = create_github_header_anchor(f"{conf.date}: {conf.name}", conf.name)
            toc += f"- {i}\n"
        return toc

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