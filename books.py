import re 
import types
import requests
from yapsy.IPlugin import IPlugin

base_url = 'https://www.googleapis.com/books/v1/'
book_search_api = base_url + 'volumes?'

class BookListener(IPlugin):
    def __init__(self):
        super(BookListener, self).__init__()
        self._matches = [re.compile('books'), re.compile('gbooks')]

    # FIXME: this API is not permenant
    def set_bot(self, bot):
        self.bot = bot
        try:
            self.dev_key = self.bot.config.get("api_keys", {}).get("google_dev_key", None)

    def call(self, regex_command, string_argument, done=None):
        if regex_command in self._matches:
            result = books(string_argument, self.dev_key)
            if isinstance(done, types.FunctionType):
                done()
            done = True
            return result, done

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
