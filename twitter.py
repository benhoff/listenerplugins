from util import hook, timesince
import tweepy
import re


@hook.command
def twitter(inp, bot=None):
    "twitter <user> [n] -- Gets last/[n]th tweet from <user>"

    consumer_key = bot.config.get("api_keys", {}).get("twitter_consumer_key")
    consumer_secret = bot.config.get("api_keys", {}).get("twitter_consumer_secret")

    oauth_token = bot.config.get("api_keys", {}).get("twitter_access_token")
    oauth_secret = bot.config.get("api_keys", {}).get("twitter_access_secret")

    if not consumer_key:
        return "Error: No Twitter API details."

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(oauth_token, oauth_secret)

    api = tweepy.API(auth)

    if re.match(r'^\w{1,15}$', inp) or re.match(r'^\w{1,15}\s+\d+$', inp):
        if inp.find(' ') == -1:
            username = inp
            tweet_number = 0
        else:
            username, tweet_number = inp.split()
            tweet_number = int(tweet_number) - 1

        if tweet_number > 300:
            return "This command can only find the last \x02300\x02 tweets."
    else:
        username = inp
        tweet_number = 0

    try:
        # try to get user by username
        user = api.get_user(username)
    except tweepy.error.TweepError as e:
        if e[0][0]['code'] == 34:
            return "Could not find user."
        else:
            return "Error {}: {}".format(e[0][0]['code'], e[0][0]['message'])

    # get the users tweets
    user_timeline = api.user_timeline(id=user.id, count=tweet_number + 1)

    # if the timeline is empty, return an error
    if not user_timeline:
        return "The user \x02{}\x02 has no tweets.".format(user.screen_name)

    # grab the newest tweet from the users timeline
    try:
        tweet = user_timeline[tweet_number]
    except IndexError:
        tweet_count = len(user_timeline)
        return "The user \x02{}\x02 only has \x02{}\x02 tweets.".format(user.screen_name, tweet_count)

    time = timesince.timesince(tweet.created_at)

    return u"@\x02{}\x02 ({}): {} ({} ago)".format(user.screen_name, user.name, tweet.text, time)


@hook.command("twinfo")
@hook.command
def twuser(inp, bot=None):
    "twuser <user> -- Get info on the Twitter user <user>"

    consumer_key = bot.config.get("api_keys", {}).get("twitter_consumer_key")
    consumer_secret = bot.config.get("api_keys", {}).get("twitter_consumer_secret")

    oauth_token = bot.config.get("api_keys", {}).get("twitter_access_token")
    oauth_secret = bot.config.get("api_keys", {}).get("twitter_access_secret")

    if not consumer_key:
        return "Error: No Twitter API details."

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(oauth_token, oauth_secret)

    api = tweepy.API(auth)

    try:
        # try to get user by username
        user = api.get_user(inp)
    except tweepy.error.TweepError as e:
        if e[0][0]['code'] == 34:
            return "Could not find user."
        else:
            return "Unknown error"

    return u"@\x02{}\x02 ({}) is located in \x02{}\x02 and has \x02{:,}\x02 tweets and \x02{:,}\x02 followers. The users description is \"{}\" " \
           "".format(user.screen_name, user.name, user.location, user.statuses_count, user.followers_count, user.description)
