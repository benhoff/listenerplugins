import re

from cloudbot import hook
from cloudbot.util import http

search_url = "http://search.atomz.com/search/?sp_a=00062d45-sp00000000"


@hook.command()
def snopes(text):
    """snopes <topic> -- Searches snopes for an urban legend about <topic>."""

    search_page = http.get_html(search_url, sp_q=text, sp_c="1")
    result_urls = search_page.xpath("//a[@target='_self']/@href")

    if not result_urls:
        return "no matching pages found"

    snopes_page = http.get_html(result_urls[0])
    snopes_text = snopes_page.text_content()

    claim = re.search(r"Claim: .*", snopes_text).group(0).strip()
    status = re.search(r"Status: .*", snopes_text)

    if status is not None:
        status = status.group(0).strip()
    else:  # new-style statuses
        status = "Status: {}.".format(re.search(r"FALSE|TRUE|MIXTURE|UNDETERMINED",
                                                snopes_text).group(0).title())

    claim = re.sub(r"[\s\xa0]+", " ", claim)  # compress whitespace
    status = re.sub(r"[\s\xa0]+", " ", status)

    return "{} {} {}".format(claim, status, result_urls[0])
