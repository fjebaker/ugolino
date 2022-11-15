import re
import bs4
import dateutil.parser

from typing import List
from ugolino import ConferenceFeed, Conference

class HEASARCFeed(ConferenceFeed):
    ROOT_URL = "https://heasarc.gsfc.nasa.gov/docs/heasarc/meetings.html"

    def conference_finder(self, soup: bs4.BeautifulSoup):
        # their website is a mess so have to go through the tags one by one
        # since nesting is meaningless
        for tag in soup.find_all(lambda t: t.name.lower() in ["dd", "dt"]):
            if tag.a is not None:
                if "name" in tag.a.attrs and re.match(r"M\d+", tag.a.attrs["name"]):
                    # this tag is the first thing that marks a conference descriptioniption
                    yield tag
    
    def parse_conference(self, info: bs4.element.Tag) -> Conference:
        title_tag = info.find(lambda t: t.name == "a" and t.b is not None)
        url = title_tag.attrs.get("href", "")
        title = title_tag.b.text
        date = None
        location = None
        description = None

        for tag in info.find_all("dd"):
            # get date
            matches = re.findall("Meeting Dates: (.+)", tag.text)
            if matches:
                date = matches[0]
                continue
            # location
            matches = re.findall("Meeting Location: (.+)", tag.text)
            if matches:
                location = matches[0]
                continue
            # description
            description = tag.text 

        return Conference(title, description, location, date, url, self.ROOT_URL)

    def scrape(self) -> List[Conference]:
        soup = self.fetch_and_parse(self.ROOT_URL)
        return [self.parse_conference(i) for i in self.conference_finder(soup)]