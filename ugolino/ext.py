# extension for python-feedgen
from feedgen.ext.base import BaseExtension


class AstroExtension(BaseExtension):
    def extend_ns(self):
        return {}
