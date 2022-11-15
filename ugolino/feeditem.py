from typing import List, Tuple
import inspect
from urllib.parse import urlparse, parse_qsl, unquote_plus


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
                fields.push(attr)
        return fields

    def __hash___(self):
        return hash(self.get_fields())
