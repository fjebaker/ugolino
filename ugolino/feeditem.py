from typing import List, Tuple
import inspect
from urllib.parse import urlparse, parse_qsl, unquote_plus
from datetime import datetime


class Url(object):
    def __init__(self, url: str):
        parts = urlparse(url)
        _path = unquote_plus(parts.path)
        # catch just "/"
        if _path.endswith("/"):
            _path = _path[0:-1]
        parts = parts._replace(query="", path=_path)
        self.parts = parts
        self.text = url

    def __eq__(self, other) -> bool:
        return self.parts == other.parts

    def __hash__(self) -> int:
        return hash(self.parts)


class FeedItem:
    Url = Url

    def get_fields(self) -> List[Tuple[str, str]]:
        fields = []
        for attr in inspect.getmembers(self):
            if not inspect.ismethod(attr[1]) and not attr[0].startswith("_"):
                fields.append(attr)
        return fields

    def __hash___(self):
        return hash(self.get_fields())

    def format_date(self):
        if hasattr(self, "date") and self.date:
            return self.date.strftime("%d %B %Y")
        return ""

    def merge(self, other: "FeedItem"):
        assert type(self) == type(other)
        for (field, _) in self.get_fields():
            f1 = self.__getattribute__(field)
            f2 = other.__getattribute__(field)

            # do nothing if other doesn't have
            if f1 and not f2:
                continue
            # overwrite if not set
            if not f1 and f2:
                self.__setattr__(field, f2)

            if type(f1) == type(f2):
                # take longest string
                if type(f1) is str:
                    if len(f2) > len(f1):
                        self.__setattr__(field, f2)
                # do nothing for datetimes
                if type(f1) is datetime:
                    continue
            else:
                logger.warn(
                    f"Comparing fields of {type(self)}: type mismatch for {field}: {type(f1)}, {type(f2)}"
                )
