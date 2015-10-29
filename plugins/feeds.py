import feedparser
import re
import types
from . import ListenerPlugin

class Feeds(ListenerPlugin):
    def __init__(self):
        super().__init__()
        self.matches = [re.compile('feed'), re.compile('rss'), re.compile('news')]

    def __call__(self, regex_command, string_argument):
        result = rss(string_argument)
        return result

def format_item(item):
    url = item.link
    title = item.title
    return "{} ({})".format(
        title, url)


def rss(text):
    """<feed> -- Gets the first three items from the RSS/ATOM feed <feed>."""
    limit = 3

    t = text.lower().strip()
    if t == "xkcd":
        addr = "http://xkcd.com/rss.xml"
    elif t == "ars":
        addr = "http://feeds.arstechnica.com/arstechnica/index"
    elif t in ("pypi", "pip", "py"):
        addr = "https://pypi.python.org/pypi?%3Aaction=rss"
        limit = 6
    elif t in ("pypinew", "pipnew", "pynew"):
        addr = "https://pypi.python.org/pypi?%3Aaction=packages_rss"
        limit = 5
    elif t == "world":
        addr = "https://news.google.com/news?cf=all&ned=us&hl=en&topic=w&output=rss"
    elif t in ("us", "usa"):
        addr = "https://news.google.com/news?cf=all&ned=us&hl=en&topic=n&output=rss"
    elif t == "nz":
        addr = "https://news.google.com/news?pz=1&cf=all&ned=nz&hl=en&topic=n&output=rss"
    elif t in ("anand", "anandtech"):
        addr = "http://www.anandtech.com/rss/"
    else:
        addr = text

    feed = feedparser.parse(addr)
    if not feed.entries:
        return "Feed not found."

    out = []
    for item in feed.entries[:limit]:
        out.append(format_item(item))

    start = "\x02{}\x02: ".format(feed.feed.title) if 'title' in feed.feed else ""
    return start + ", ".join(out)
