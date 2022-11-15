from typing import Union, List
from datetime import datetime


def try_parse(date: str, patterns: List[str]) -> Union[None, datetime]:
    for pattern in patterns:
        try:
            d = datetime.strptime(date, pattern)
        except ValueError:
            continue
        else:
            return d
    return None
