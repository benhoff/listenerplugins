from util import hook, web, http


@hook.command('gfy')
@hook.command
def lmgtfy(inp):
    """lmgtfy [phrase] - Posts a google link for the specified phrase"""

    link = "http://lmgtfy.com/?q=%s" % http.quote_plus(inp)

    try:
        return web.isgd(link)
    except (web.ShortenError, http.HTTPError):
        return link
