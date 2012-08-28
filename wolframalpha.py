import re

from util import hook, http

from urllib import quote_plus
from urllib2 import HTTPError
from util.web import isgd
from util.text import truncate_words


@hook.command('wa')
@hook.command
def wolframalpha(inp, bot=None):
    "wa <query> -- Computes <query> using Wolfram Alpha."

    api_key = bot.config.get("api_keys", {}).get("wolframalpha", None)

    if not api_key:
        return "error: missing api key"

    url = 'http://api.wolframalpha.com/v2/query?format=plaintext'

    result = http.get_xml(url, input=inp, appid=api_key)

    # get the URL for a user to view this query in a browser
    query_url = "http://www.wolframalpha.com/input/?i=" + \
                quote_plus(inp.encode('utf-8'))
    try:
        short_url = isgd(query_url)
    except (HTTPError):
        short_url = query_url

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
        return unichr(int(match.group(1), 16))

    ret = re.sub(r'\\:([0-9a-z]{4})', unicode_sub, ret)

    ret = truncate_words(ret, 410)
    
    if not ret:
        return 'No results.'

    return "%s - %s" % (ret, short_url)
