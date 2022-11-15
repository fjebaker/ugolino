from typing import Union, List
from datetime import datetime

from urllib.parse import urlparse, unquote_plus


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


def try_parse(date: str, patterns: List[str]) -> Union[None, datetime]:
    for pattern in patterns:
        try:
            d = datetime.strptime(date, pattern)
        except ValueError:
            continue
        else:
            return d
    return None
