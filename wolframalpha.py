import re

from cloudbot import hook
from cloudbot.util import http, web, formatting


@hook.command("wa", "calc", "math", "wolframalpha")
def wolframalpha(text, bot):
    """wa <query> -- Computes <query> using Wolfram Alpha."""
    api_key = bot.config.get("api_keys", {}).get("wolframalpha", None)

    if not api_key:
        return "error: missing api key"

    url = 'http://api.wolframalpha.com/v2/query?format=plaintext'

    result = http.get_xml(url, input=text, appid=api_key)

    # get the URL for a user to view this query in a browser
    query_url = "http://www.wolframalpha.com/input/?i=" + \
                http.quote_plus(text.encode('utf-8'))
    short_url = web.try_shorten(query_url)

    pod_texts = []
    for pod in result.xpath("//pod[@primary='true']"):
        title = pod.attrib['title']
        if pod.attrib['id'] == 'Input':
            continue

        results = []
        for subpod in pod.xpath('subpod/plaintext/text()'):
            subpod = subpod.strip().replace('\\n', '; ')
            subpod = re.sub(r'\s+', ' ', subpod)
            if subpod:
                results.append(subpod)
        if results:
            pod_texts.append(title + ': ' + ', '.join(results))

    ret = ' - '.join(pod_texts)

    if not pod_texts:
        return 'No results.'

    ret = re.sub(r'\\(.)', r'\1', ret)

    def unicode_sub(match):
        return chr(int(match.group(1), 16))

    ret = re.sub(r'\\:([0-9a-z]{4})', unicode_sub, ret)

    ret = formatting.truncate_str(ret, 250)

    if not ret:
        return 'No results.'

    return "{} - {}".format(ret, short_url)
