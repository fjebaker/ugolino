# set up logger with colour
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

from ugolino.feed import AbstractFeed
from ugolino.feeditem import FeedItem
from ugolino.conferences import Conference, ConferenceFeed
from ugolino.seminars import Seminar, SeminarFeed
from ugolino.aggregator import Aggregator
