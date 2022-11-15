from typing import List, Tuple
import inspect

class FeedItem:
        
    def get_fields(self) -> List[Tuple[str, str]]:
        fields = []
        for attr in inspect.getmembers(self):
            if not inspect.ismethod(attr[1]) and not attr[0].startswith("_"):
                fields.push(attr)
        return fields

    def to_markdown(self):
        ... 

    def to_rss():
        ...