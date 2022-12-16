from ugolino.feeds.conference_heasarc import HEASARCFeed
from ugolino.feeds.conference_cacd import CACDFeed
from ugolino.feeds.seminar_vast import VASTFeed
from ugolino.feeds.seminar_iauiaa import IAUAIIFeed
from ugolino.feeds.conference_athena import AthenaFeed

conference_feeds = [HEASARCFeed, CACDFeed, AthenaFeed]

seminar_feeds = [VASTFeed, IAUAIIFeed]
