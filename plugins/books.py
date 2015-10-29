import re 
import types
import requests
from . import ListenerPlugin

base_url = 'https://www.googleapis.com/books/v1/'
book_search_api = base_url + 'volumes?'

class Books(ListenerPlugin):
    CONFIG_TEMPLATE = {'Google API Key': None}

    def __init__(self):
        super().__init__()
        self.matches = [re.compile('books'), re.compile('gbooks')]
        self._api_key = 'Google API Key'
        self.config = self.CONFIG_TEMPLATE

    def __call__(self, regex_command, string_argument):
        result = books(string_argument, self.config[self._api_key])
        return result

def books(text, dev_key=None):
    """books <query> -- Searches Google Books for <query>."""
    if not dev_key:
        return "This command requires a Google Developers Console API key."

    json = requests.get(book_search_api, params={"q": text, "key": dev_key, "country": "US"}).json()

    if json.get('error'):
        if json['error']['code'] == 403:
            print(json['error']['message'])
            return "The Books API is off in the Google Developers Console (or check the console)."
        else:
            return 'Error performing search.'

    if json['totalItems'] == 0:
        return 'No results found.'

    book = json['items'][0]['volumeInfo']
    title = book['title']
    try:
        author = book['authors'][0]
    except KeyError:
        try:
            author = book['publisher']
        except KeyError:
            author = "Unknown Author"

    try:
        description = book['description']
    except KeyError:
        description = "No description available."

    try:
        year = book['publishedDate'][:4]
    except KeyError:
        year = "No Year"

    try:
        page_count = book['pageCount']
        pages = ' - \x02{:,}\x02 page{}'.format(page_count, "s"[page_count == 1:])
    except KeyError:
        pages = ''

    link = book['infoLink']
    #link = web.shorten(book['infoLink'], service="goo.gl", key=dev_key)

    return "\x02{}\x02 by \x02{}\x02 ({}){} - {} - {}".format(title, author, year, pages, description, link)
