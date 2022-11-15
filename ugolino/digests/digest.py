import abc

from ugolino import Conference


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
    def drain(self) -> str:
        ...

    # ... todo: others

    def digest(self) -> str:
        self.setup()
        for conf in self.aggregator.conferences:
            self.conference(conf)

        content = self.header()
        content += self.drain()
        content += self.suffix()

        return content
