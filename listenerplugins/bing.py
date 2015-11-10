import re
import random

import requests
from lxml import html

from . import ListenerPlugin

API_URL = "https://api.datamarket.azure.com/Bing/Search/v1/Composite"

# filters for SafeSearch
# DEFAULT_FILTER is used unless a user appends " nsfw" to a search term, then the NSFW_FILTER is used
# use ("Moderate", "Off") to allow searching NSFW content with the NSFW search tag
# use ("Strict", "Strict") to block all NSFW content
# the default config just sets the filter to Moderate for all queries
DEFAULT_FILTER = "Moderate"
NSFW_FILTER = "Moderate"


class Bing(ListenerPlugin):
    CONFIG_TEMPLATE = {'Bing API key': None}

    def __init__(self):
        super().__init__()
        self._bing_matches = [re.compile('bing'), re.compile('b')]
        self._bing_img_matches = [re.compile('bingimage'), re.compile('bis')]
        self.matches = []
        self.matches.extend(self._bing_img_matches)
        self.matches.extend(self._bing_matches)
        self.config = self.CONFIG_TEMPLATE
        self._api_key ='Bing API key' 

    def __call__(self, regex_command, string_argument):
        if regex_command in self._bing_matches:
            result = bing(string_argument, self.config[self._api_key])
        elif regex_command in self._bing_img_matches:
            result = bingimage(string_argument, self.config[self._api_key])
        return result


def unescape(s):
    if not s.strip():
        return s
    return html.fromstring(s).text_content()


def bingify(s):
    """ because bing has to be an asshole and require special params """
    return "'{}'".format(s)


def bing(text, api_key):
    """<query> - returns the first bing search result for <query>"""
    # handle NSFW
    show_nsfw = text.endswith(" nsfw")
    # remove "nsfw" from the input string after checking for it
    if show_nsfw:
        text = text[:-5].strip().lower()

    rating = NSFW_FILTER if show_nsfw else DEFAULT_FILTER

    if not api_key:
        return "Error: No Bing Azure API details."

    # why are these all differing formats and why does format have a $? ask microsoft
    params = {
        "Sources": bingify("web"),
        "Query": bingify(text),
        "Adult": bingify(rating),
        "$format": "json"
    }

    request = requests.get(API_URL, params=params, auth=(api_key, api_key))

    # I'm not even going to pretend to know why results are in ['d']['results'][0]
    j = request.json()['d']['results'][0]

    if not j["Web"]:
        return "No results."

    result = j["Web"][0]

    # not entirely sure this even needs un-escaping, but it wont hurt to leave it in
    title = unescape(result["Title"])
    desc = unescape(result["Description"])
    url = unescape(result["Url"])

    return '{} -- $(b){}$(b): "{}"'.format(url, title, desc)


def bingimage(text, api_key):
    """<query> - returns the first bing image search result for <query>"""

    # handle NSFW
    show_nsfw = text.endswith(" nsfw")

    # remove "nsfw" from the input string after checking for it
    if show_nsfw:
        text = text[:-5].strip().lower()

    rating = NSFW_FILTER if show_nsfw else DEFAULT_FILTER

    if not api_key:
        return "Error: No Bing Azure API details."

    # why are these all differing formats and why does format have a $? ask microsoft
    params = {
        "Sources": bingify("image"),
        "Query": bingify(text),
        "Adult": bingify(rating),
        "$format": "json"
    }

    request = requests.get(API_URL, params=params, auth=(api_key, api_key))

    # I'm not even going to pretend to know why results are in ['d']['results'][0]
    j = request.json()['d']['results'][0]

    if not j["Image"]:
        return "No results."

    # grab a random result from the top 10
    result = random.choice(j["Image"][:10])

    # output stuff
    tags = []

    # image size
    tags.append("{}x{}px".format(result["Width"], result["Height"]))
    # file type
    tags.append(result["ContentType"])
    # file size
    # tags.append(filesize.size(int(result["FileSize"]), system=filesize.alternative))
    # NSFW warning
    if "explicit" in result["Thumbnail"]["MediaUrl"]:
        tags.append("NSFW")

    # join all the tags together in a comma separated string ("tag1, tag2, tag3")
    tag_text = ", ".join(tags)

    return '{} ({})'.format(unescape(result["MediaUrl"]), tag_text)
