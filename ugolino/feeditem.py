import re
import inspect
from typing import List, Tuple
from datetime import datetime

import logging

logger = logging.Logger(__name__)


class FeedItem:
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

    def clean(self, i: str) -> str:
        return re.sub("\s+", " ", i.strip().replace("\n", " "))

    def merge_with(self, other: "FeedItem"):
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
