from util import hook, http
import time
from util.text import capitalize_first

api_url = 'http://api.wolframalpha.com/v2/query?format=plaintext'


@hook.command("time")
def time_command(inp, bot=None):
    "time <area> -- Gets the time in <area>"

    query = "current time in %s" % inp

    api_key = bot.config.get("api_keys", {}).get("wolframalpha", None)
    if not api_key:
        return "error: no wolfram alpha api key set"

    request = http.get_xml(api_url, input=query, appid=api_key)
    time = " ".join(request.xpath("//pod[@title='Result']/subpod/plain" \
                    "text/text()"))
    time = time.replace("  |  ", ", ")

    if time:
        # nice place name for UNIX time
        if inp.lower() == "unix":
            place = "Unix Epoch"
        else:
            place = capitalize_first(" ".join(request.xpath("//pod[@" \
                "title='Input interpretation']/subpod/plaintext/text()"))[16:])
        return "%s - \x02%s\x02" % (time, place)
    else:
        return "Could not get the time for '%s'." % inp


@hook.command(autohelp=False)
def beats(inp):
    "beats -- Gets the current time in .beats (Swatch Internet Time). "

    if inp.lower() == "wut":
        return "Instead of hours and minutes, the mean solar day is divided " \
        "up into 1000 parts called \".beats\". Each .beat lasts 1 minute and" \
        " 26.4 seconds. Times are notated as a 3-digit number out of 1000 af" \
        "ter midnight. So, @248 would indicate a time 248 .beats after midni" \
        "ght representing 248/1000 of a day, just over 5 hours and 57 minute" \
        "s. There are no timezones."

    t = time.gmtime()
    h, m, s = t.tm_hour, t.tm_min, t.tm_sec

    utc = 3600 * h + 60 * m + s
    bmt = utc + 3600  # Biel Mean Time (BMT)

    beat = bmt / 86.4

    if beat > 1000:
        beat -= 1000

    return "\x02Swatch Internet Time:\x02 @%06.2f" % beat
