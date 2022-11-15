from typing import List
from ugolino.digests import Digest
from ugolino import Conference, Seminar


class MarkdownDigest(Digest):
    def sanitize(self, s: str) -> str:
        return s.replace(":", "")

    def create_header_anchor(self, title, header_title):
        return "[{}](#{})".format(
            title, self.sanitize(header_title.strip().replace(" ", "-"))
        )

    def header(self) -> str:
        toc = f"## {self.title}\n\n### Table of contents\n\n"
        for i in self.toc_items:
            toc += f"- {i}\n"
        return toc + "\n\n"

    def setup(self, title: str):
        self.toc_items: List[str] = []
        self.body: List[str] = []
        self.title = title

    def drain(self) -> str:
        return "\n\n".join(self.body)

    def conference(self, conf: Conference) -> None:
        date = conf.format_date()
        # create toc entry
        self.toc_items.append(
            self.create_header_anchor(f"{date}: {conf.name}", conf.name)
        )

        s = f"### {conf.name}\n\n"
        s += f"- Date: {date}\n"
        s += f"- Location: {conf.location}\n"
        if conf.link:
            s += f"- [See this link]({conf.link.text}) for more info.\n"
        s += "\n"
        s += f"{conf.description}\n"
        s += "\n"
        s += f"[Source]({conf.source})\n"

        self.body.append(s)

    def seminar(self, sem: Seminar) -> None:
        date = sem.format_date()
        self.toc_items.append(
            self.create_header_anchor(f"{date}: {sem.speaker} - {sem.title}", sem.title)
        )

        s = f"### {sem.title}\n\n"
        s += f"- Date: {date}\n"
        s += f"- Speaker: {sem.speaker}\n"
        s += f"- Location: {sem.location}\n"
        if sem.link:
            s += f"- [See this link]({sem.link.text}) for more info.\n"
        s += "\n"
        s += f"{sem.description}\n"
        s += "\n"
        s += f"[Source]({sem.source})\n"

        self.body.append(s)
