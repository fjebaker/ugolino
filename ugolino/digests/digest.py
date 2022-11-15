import abc

from ugolino import Conference


class Digest(abc.ABC):
    def __init__(self, aggregator):
        self.aggregator = aggregator

    def setup(self) -> None:
        return

    def header(self) -> str:
        return ""

    def suffix(self) -> str:
        return ""

    @abc.abstractmethod
    def conference(self, conf: Conference):
        ...

    # ... todo: others

    def digest(self) -> str:
        self.setup()
        confs = [self.conference(conf) for conf in self.aggregator.conferences]

        content = self.header()
        content += "\n\n".join(confs)
        content += self.suffix()

        return content
