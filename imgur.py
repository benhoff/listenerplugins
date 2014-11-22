import re
import random

from cloudbot import hook
from cloudbot.util import http, web

base_url = "http://reddit.com/r/{}/.json"
imgur_re = re.compile(r'http://(?:i\.)?imgur\.com/(a/)?(\w+\b(?!/))\.?\w?')

album_api = "https://api.imgur.com/3/album/{}/images.json"


def is_valid(data):
    if data["domain"] in ["i.imgur.com", "imgur.com"]:
        return True
    else:
        return False


@hook.command(autohelp=False)
def imgur(text):
    """[subreddit] - returns a link to the first page of imgur images from [subreddit],
     or the first page of all imgur images if no subreddit is provided"""
    if text:
        # see if the input ends with "nsfw"
        show_nsfw = text.endswith(" nsfw")

        # remove "nsfw" from the input string after checking for it
        if show_nsfw:
            text = text[:-5].strip().lower()

        url = base_url.format(text.strip())
    else:
        url = "http://www.reddit.com/domain/imgur.com/.json"
        show_nsfw = False

    try:
        data = http.get_json(url, user_agent=http.ua_chrome)
    except Exception as e:
        return "Error: " + str(e)

    data = data["data"]["children"]
    random.shuffle(data)

    # filter list to only have imgur links
    filtered_posts = [i["data"] for i in data if is_valid(i["data"])]

    if not filtered_posts:
        return "No images found."

    items = []

    headers = {
        "Authorization": "Client-ID b5d127e6941b07a"
    }

    # loop over the list of posts
    for post in filtered_posts:
        if post["over_18"] and not show_nsfw:
            continue

        match = imgur_re.search(post["url"])
        if match.group(1) == 'a/':
            # post is an album
            url = album_api.format(match.group(2))
            images = http.get_json(url, headers=headers)["data"]

            # loop over the images in the album and add to the list
            for image in images:
                items.append(image["id"])

        elif match.group(2) is not None:
            # post is an image
            items.append(match.group(2))

    if not items:
        return "No images found (use .imgur <subreddit> nsfw to show explicit content)"

    if show_nsfw:
        return "{} \x02NSFW\x02".format(web.try_shorten("http://imgur.com/" + ','.join(items)))
    else:
        return web.try_shorten("http://imgur.com/" + ','.join(items))
