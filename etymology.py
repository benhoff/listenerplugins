# Plugin by GhettoWizard and Scaevolus

import re
from lxml import html

import requests
from yapsy.IPlugin import IPlugin

class EtymologyListener(IPlugin):
    def __init__(self):
        super(EtymologyListener, self).__init__()
        self._matches = [re.compile('e'), re.compile('etymology')]

    # FIXME: this API is not permenant
    def set_bot(self, bot):
        self.bot = bot

    def call(self, regex_command, string_argument):
        if regex_command in self._matches:
            return etymology(string_argument)

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
