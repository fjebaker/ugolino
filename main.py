import logging
LOG_LEVEL = logging.DEBUG
LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
from colorlog import ColoredFormatter
logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter(LOGFORMAT)
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
log = logging.getLogger('pythonConfig')
log.setLevel(LOG_LEVEL)
log.addHandler(stream)

import sys
import subprocess
import ugolino
from ugolino.feeds import HEASARCFeed, CACDFeed
from typing import List


def run(cmd: List[str]) -> None:
    process = subprocess.Popen(
        cmd, stderr=sys.stderr, stdout=sys.stdout, cwd="./astro-feeds"
    )
    process.wait()


def update_feed_repo():
    run("git add --all .".split())
    run("git config user.name ugolino".split())
    run("git config user.email ugolino@cosroe.com".split())
    run(["git", "commit", "-m", "updated README feed aggregate"])
    run("git push origin ugolino-feed".split())


global_toc = """# Astro feeds

Aggregated feeds of events related to astrophysics and astronomy.

Automatically curated and updated using [fjebaker/ugolino](https://github.com/fjebaker/ugolino). Please open requests on the ugolino repository, and issues related to specific items on this repository.

## Contents
- [Seminars](#Seminars)
- [Conferences](#Conferences)

<hr>

"""

if __name__ == "__main__":
    aggregator = ugolino.Aggregator()

    # aggregator.fetch("iauiaa")
    aggregator.fetch_all()
    aggregator.filter_unique()
    aggregator.sort()

    rss_seminars = aggregator.rss.digest("seminars")
    rss_conferences = aggregator.rss.digest("conferences")
    md_seminars = aggregator.markdown.digest("seminars")
    md_conferences = aggregator.markdown.digest("conferences")

    with open("astro-feeds/conferences-rss.xml", "w") as f:
        f.write(rss_conferences)
    with open("astro-feeds/seminars-rss.xml", "w") as f:
        f.write(rss_seminars)
    with open("astro-feeds/README.md", "w") as f:
        f.write(global_toc)
        f.write(md_seminars)
        f.write("\n<hr>\n\n")
        f.write(md_conferences)
    update_feed_repo()
