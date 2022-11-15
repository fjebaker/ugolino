from typing import List
from ugolino.digests import Digest
from ugolino import Conference


class MarkdownDigest(Digest):
    def sanitize(self, s: str) -> str:
        return s.replace(":", "")

    def create_header_anchor(self, title, header_title):
        return "[{}](#{})".format(
            title, self.sanitize(header_title.strip().replace(" ", "-"))
        )

    def create_toc(self) -> str:
        toc = "## Table of Contents\n"
        for conf in self.conferences:
            i = self.create_header_anchor(f"{conf.date}: {conf.name}", conf.name)
            toc += f"- {i}\n"
        return toc

    def header(self) -> str:
        toc = "## Conferences\n\n### Table of contents\n\n"
        for i in self.toc_items:
            toc += f"- {i}\n"
        return toc + "\n\n"

    def setup(self):
        self.toc_items: List[str] = []
        self.body: List[str] = []

    def drain(self) -> str:
        return "\n\n".join(self.body)

    def conference(self, conf: Conference) -> None:
        # create toc entry
        self.toc_items.append(
            self.create_header_anchor(f"{conf.date}: {conf.name}", conf.name)
        )

        s = f"### {conf.name}\n\n"
        s += f"- Date: {conf.date}\n"
        s += f"- Location: {conf.location}\n"
        if conf.link:
            s += f"- [See this link]({conf.link.text}) for more info.\n"
        s += "\n"
        s += f"{conf.description}\n"
        s += "\n"
        s += f"[Source]({conf.source})\n"
        
        self.body.append(s)