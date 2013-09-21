import re
import time

from util import hook, http


youtube_re = (r'(?:youtube.*?(?:v=|/v/)|youtu\.be/|yooouuutuuube.*?id=)'
              '([-_a-zA-Z0-9]+)', re.I)

base_url = 'http://gdata.youtube.com/feeds/api/'
api_url = base_url + 'videos/{}?v=2&alt=jsonc'
search_api_url = base_url + 'videos?v=2&alt=jsonc&max-results=1'
video_url = "http://youtu.be/%s"


def get_video_description(video_id):
    request = http.get_json(api_url.format(video_id))

    if request.get('error'):
        return

    data = request['data']

    out = '\x02%s\x02' % data['title']

    if not data.get('duration'):
        return out

    out += ' - length \x02'
    length = data['duration']
    if length / 3600:  # > 1 hour
        out += '%dh ' % (length / 3600)
    if length / 60:
        out += '%dm ' % (length / 60 % 60)
    out += "%ds\x02" % (length % 60)

    if 'rating' in data:
        out += ' - rated \x02%.2f/5.0\x02 (%d)' % (data['rating'],
                                                   data['ratingCount'])

    if 'viewCount' in data:
        out += ' - \x02%s\x02 views' % format(data['viewCount'], ",d")

    try:
        uploader = http.get_json(base_url + "users/{}?alt=json".format(data["uploader"]))["entry"]["title"]["$t"]
    except:
        uploader = data["uploader"]

    upload_time = time.strptime(data['uploaded'], "%Y-%m-%dT%H:%M:%S.000Z")
    out += ' - \x02%s\x02 on \x02%s\x02' % (uploader,
                                            time.strftime("%Y.%m.%d", upload_time))

    if 'contentRating' in data:
        out += ' - \x034NSFW\x02'

    return out


def GetInHMS(seconds):
    hours = seconds / 3600
    seconds -= 3600 * hours
    minutes = seconds / 60
    seconds -= 60 * minutes
    if hours == 0:
        return "%02d:%02d" % (minutes, seconds)
    return "%02d:%02d:%02d" % (hours, minutes, seconds)


@hook.regex(*youtube_re)
def youtube_url(match):
    return get_video_description(match.group(1))


@hook.command('yt')
@hook.command('y')
@hook.command
def youtube(inp):
    """youtube <query> -- Returns the first YouTube search result for <query>."""

    request = http.get_json(search_api_url, q=inp)

    if 'error' in request:
        return 'error performing search'

    if request['data']['totalItems'] == 0:
        return 'no results found'

    video_id = request['data']['items'][0]['id']

    return get_video_description(video_id) + " - " + video_url % video_id


ytpl_re = (r'(.*:)//(www.youtube.com/playlist|youtube.com/playlist)(:[0-9]+)?(.*)', re.I)


@hook.regex(*ytpl_re)
def ytplaylist_url(match):
    location = match.group(4).split("=")[-1]
    try:
        soup = http.get_soup("https://www.youtube.com/playlist?list=" + location)
    except Exception:
        return "\x034\x02Invalid response."
    title = soup.find('title').text.split('-')[0].strip()
    author = soup.find('img', {'class': 'channel-header-profile-image'})['title']
    numvideos = soup.find('ul', {'class': 'header-stats'}).findAll('li')[0].text.split(' ')[0]
    views = soup.find('ul', {'class': 'header-stats'}).findAll('li')[1].text.split(' ')[0]
    return u"\x02%s\x02 - \x02%s\x02 views - \x02%s\x02 videos - \x02%s\x02" % (title, views, numvideos, author)
