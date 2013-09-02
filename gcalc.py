from util import hook, http

@hook.command("math")
@hook.command
def calc(inp):
    "calc <term> -- Calculate <term> with Google Calc."

    soup = http.get_soup('http://www.google.com/search', q=inp)

    result = soup.find('h2', {'class': 'r'})
    exponent = result.find('sup')
    if not result:
        return "Could not calculate '%s'" % inp

    if not exponent:
        return result.contents[0]
    if exponent:
        return result.contents[0] + "^" + exponent.contents[0]
