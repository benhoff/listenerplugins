# Plugin by https://github.com/Mu5tank05
from cloudbot import hook
from cloudbot.util import web, http


@hook.command("qrcode", "qr")
def qrcode(text):
    """[link] - returns a link to a QR code image for [link]"""

    args = {
        "cht": "qr",  # chart type (QR)
        "chs": "200x200",  # dimensions
        "chl": text  # data
    }

    link = http.prepare_url("http://chart.googleapis.com/chart", args)
    return web.try_shorten(link)
