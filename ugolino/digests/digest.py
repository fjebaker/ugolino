import abc

from ugolino import Conference, Seminar


class Digest(abc.ABC):
    def __init__(self, aggregator):
        self.aggregator = aggregator

    def header(self) -> str:
        return ""

    def suffix(self) -> str:
        return ""

    @abc.abstractmethod
    def setup(self) -> None:
        ...

    @abc.abstractmethod
    def conference(self, conf: Conference) -> None:
        ...

    @abc.abstractmethod
    def seminar(self, conf: Seminar) -> None:
        ...

    @abc.abstractmethod
    def drain(self) -> str:
        ...

    # ... todo: others

    def add_conferences(self):
        for conf in self.aggregator.conferences:
            self.conference(conf)

    def add_seminars(self):
        for sem in self.aggregator.seminars:
            self.seminar(sem)

    def digest(self, what="all") -> str:
        if what == "conferences":
            self.setup("Conferences")
            self.add_conferences()
        elif what == "seminars":
            self.setup("Seminars")
            self.add_seminars()
        elif what == "all":
            self.setup("All")
            self.add_conferences()
            self.add_seminars()
        else:
            raise Exception(f"Unknown digest {what}")

        content = self.header()
        content += self.drain()
        content += self.suffix()

        return content
