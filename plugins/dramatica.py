import re
import types
from urllib import parse
from lxml import html

import requests
from . import ListenerPlugin

api_url = "http://encyclopediadramatica.se/api.php"
ed_url = "http://encyclopediadramatica.se/"

class Drama(ListenerPlugin):
    def __init__(self):
        super(Drama, self).__init__()
        self._matches = [re.compile('drama'),]

    def call(self, regex_command, string_argument, done=None):
        if regex_command in self._matches:
            result = drama(string_argument)
            if isinstance(done, types.FunctionType):
                done()
            done = True
            return result, done

def drama(text):
    """<phrase> - gets the first paragraph of the Encyclopedia Dramatica article on <phrase>"""

    search_response = requests.get(api_url, params={"action": "opensearch", "search": text})

    if search_response.status_code != requests.codes.ok:
        return "Error searching: {}".format(search_response.status_code)

    data = search_response.json()

    if not data[1]:
        return "No results found."
    article_name = data[1][0].replace(' ', '_')

    url = ed_url + parse.quote(article_name, '')

    page_response = requests.get(url)

    if page_response.status_code != requests.codes.ok:
        return "Error getting page: {}".format(page_response.status_code)

    page = html.fromstring(page_response.text)

    for p in page.xpath('//div[@id="bodyContent"]/p'):
        if p.text_content():
            summary = " ".join(p.text_content().splitlines())
            summary = re.sub("\[\d+\]", "", summary)
            #summary = summary
            return "{} - {}".format(summary, url)

    return "Unknown Error."
