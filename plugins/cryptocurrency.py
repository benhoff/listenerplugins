"""
cryptocurrency.py

A plugin that uses the CoinMarketCap JSON API to get values for cryptocurrencies.

Created By:
    - Luke Rogers <https://github.com/lukeroge>

Special Thanks:
    - https://coinmarketcap-nexuist.rhcloud.com/

License:
    GPL v3
"""
import types
from urllib.parse import quote_plus
from datetime import datetime
import re

import requests
from . import ListenerPlugin

API_URL = "https://coinmarketcap-nexuist.rhcloud.com/api/{}"

class Cryptocurrency(ListenerPlugin):
    def __init__(self):
        super().__init__()
        self._bitcoin_matches = [re.compile('bitcoin'), re.compile('btc')]
        self._litecoin_matches = [re.compile('litecoin'), re.compile('ltc')]
        self._doge_matches = [re.compile('dogecoin'), re.compile('doge')]

        self.matches = [re.compile('crypto'), re.compile('cryptocurrency')]

        self.matches.extend(self._bitcoin_matches)
        self.matches.extend(self._litecoin_matches)
        self.matches.extend(self._doge_matches)

    def __call__(self, regex_command, string_argument):
        if regex_command in self._bitcoin_matches:
            result = crypto_command('btc')
        elif regex_command in self._doge_matches:
            result = crypto_command("doge")
        elif regex_command in self._litecoin_matches:
            result = crypto_command("ltc")
        else:
            result = crypto_command(string_argument)

        return result


# main command
def crypto_command(text):
    """ <ticker> -- Returns current value of a cryptocurrency """
    try:
        encoded = quote_plus(text)
        request = requests.get(API_URL.format(encoded))
        request.raise_for_status()
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        return "Could not get value: {}".format(e)

    data = request.json()

    if "error" in data:
        return "{}.".format(data['error'])

    updated_time = datetime.fromtimestamp(data['timestamp'])
    if (datetime.today() - updated_time).days > 2:
        # the API retains data for old ticker names that are no longer updated
        # in these cases we just return a "not found" message
        return "Currency not found."

    change = float(data['change'])
    if change > 0:
        change_str = "\x033 {}%\x0f".format(change)
    elif change < 0:
        change_str = "\x035 {}%\x0f".format(change)
    else:
        change_str = "{}%".format(change)

    return "{} // \x0307${:,.2f}\x0f USD - {:,.7f} BTC // {} change".format(data['symbol'].upper(),
                                                                            float(data['price']['usd']),
                                                                            float(data['price']['btc']),
                                                                            change_str)
