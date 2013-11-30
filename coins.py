from util import http, hook


@hook.command("butt", autohelp=False)
@hook.command("btc", autohelp=False)
@hook.command(autohelp=False)
def bitcoin(inp):
    "bitcoin <exchange> -- Gets current exchange rate for bitcoins from several exchanges, default is Blockchain. Supports MtGox, Bitpay, Coinbase and BitStamp."
    exchanges = {
        "blockchain": {
            "api_url": "https://blockchain.info/ticker",
            "func": lambda data: u"Blockchain // Buy: \x0307${:,.2f}\x0f - Sell: \x0307${:,.2f}\x0f".format(data["USD"]["buy"], \
                                   data["USD"]["sell"])
        },
        "mtgox": {
            "api_url": "https://mtgox.com/api/1/BTCUSD/ticker",
            "func": lambda data: u"MtGox // Current: \x0307{}\x0f - High: \x0307{}\x0f - Low: \x0307{}\x0f - Best Ask: \x0307{}\x0f - Volume: {}".format(data['return']['last']['display'], \
                                   data['return']['high']['display'], data['return']['low']['display'], data['return']['buy']['display'], \
                                   data['return']['vol']['display'])
        },
        "coinbase":{
            "api_url": "https://coinbase.com/api/v1/prices/spot_rate",
            "func": lambda data: u"Coinbase // Current: \x0307${:,.2f}\x0f".format(float(data['amount']))
        },
        "bitpay": {
            "api_url": "https://bitpay.com/api/rates",
            "func": lambda data: u"Bitpay // Current: \x0307${:,.2f}\x0f".format(data[0]['rate'])
        },
        "bitstamp": {
            "api_url": "https://www.bitstamp.net/api/ticker/",
            "func": lambda data: u"BitStamp // Current: \x0307${:,.2f}\x0f - High: \x0307${:,.2f}\x0f - Low: \x0307${:,.2f}\x0f - Volume: {:,.2f} BTC".format(float(data['last']), float(data['high']), float(data['low']), \
                                   float(data['volume']))
        }
    }

    inp = inp.lower()

    if inp:
        if inp in exchanges:
            exchange = exchanges[inp]
        else:
            return "Invalid Exchange"
    else:
        exchange = exchanges["blockchain"]

    data = http.get_json(exchange["api_url"])
    func = exchange["func"]
    return func(data)


@hook.command(autohelp=False)
def litecoin(inp, message=None):
    """litecoin -- gets current exchange rate for litecoins from BTC-E"""
    data = http.get_json("https://btc-e.com/api/2/ltc_usd/ticker")
    ticker = data['ticker']
    message("Current: \x0307${:,.2f}\x0f - High: \x0307${:,.2f}\x0f"
        " - Low: \x0307${:,.2f}\x0f - Volume: {:,.2f} LTC".format(ticker['buy'], ticker['high'], ticker['low'], ticker['vol_cur']))
