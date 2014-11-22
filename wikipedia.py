"""Searches wikipedia and returns first sentence of article
Scaevolus 2009"""

import re

from cloudbot import hook
from cloudbot.util import http, formatting

api_prefix = "http://en.wikipedia.org/w/api.php"
search_url = api_prefix + "?action=opensearch&format=xml"

paren_re = re.compile('\s*\(.*\)$')


@hook.command("wiki", "wikipedia", "w")
def wiki(text):
    """wiki <phrase> -- Gets first sentence of Wikipedia article on <phrase>."""

    x = http.get_xml(search_url, search=text)

    ns = '{http://opensearch.org/searchsuggest2}'
    items = x.findall(ns + 'Section/' + ns + 'Item')

    if not items:
        if x.find('error') is not None:
            return 'error: %(code)s: %(info)s' % x.find('error').attrib
        else:
            return 'No results found.'

    def extract(item):
        return [item.find(ns + i).text for i in
                ('Text', 'Description', 'Url')]

    title, desc, url = extract(items[0])

    if 'may refer to' in desc:
        title, desc, url = extract(items[1])

    title = paren_re.sub('', title)

    if title.lower() not in desc.lower():
        desc = title + desc

    desc = ' '.join(desc.split())  # remove excess spaces

    desc = formatting.truncate_str(desc, 200)

    return '{} :: {}'.format(desc, http.quote(url, ':/'))
