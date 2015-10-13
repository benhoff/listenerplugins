# Plugin by GhettoWizard and Scaevolus
import types
import re
from lxml import html

import requests
from . import ListenerPlugin

class Etymology(ListenerPlugin):
    def __init__(self):
        super(Etymology, self).__init__()
        self._matches = [re.compile('e'), re.compile('etymology')]

    def call(self, regex_command, string_argument, done=None):
        if regex_command in self._matches:
            result = etymology(string_argument)
            if isinstance(done, types.FunctionType):
                done()
            done = True
            return result, done

def etymology(text):
    """<word> - retrieves the etymology of <word>
    :type text: str
    """

    url = 'http://www.etymonline.com/index.php'

    response = requests.get(url, params={"term": text})
    if response.status_code != requests.codes.ok:
        return "Error reaching etymonline.com: {}".format(response.status_code)

    h = html.fromstring(response.text)

    etym = h.xpath('//dl')

    if not etym:
        return 'No etymology found for {} :('.format(text)

    etym = etym[0].text_content()

    etym = ' '.join(etym.split())

    if len(etym) > 400:
        etym = etym[:etym.rfind(' ', 0, 400)] + ' ...'

    return etym
