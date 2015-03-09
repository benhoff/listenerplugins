import re
import random

import requests

from cloudbot import hook
from cloudbot.util import web


BASE_URL = 'http://api.wordnik.com/v4/'


@hook.on_start()
def load_key(bot):
    global api_key
    api_key = bot.config.get("api_keys", {}).get("wordnik", None)


@hook.command("define", "dictionary")
def define(text):
    """<word> -- Returns a dictionary definition for <word>."""
    if not api_key:
        return "This command requires an API key from wordnik.com."
    word = text.split(' ')[0]
    url = BASE_URL + "word.json/{}/definitions".format(word)
    dictionaries = {
        'ahd-legacy': 'The American Heritage Dictionary',
        'century': 'The Century Dictionary',
        'wiktionary': 'Wiktionary',
        'gcide': 'Collaborative International Dictionary of English',
        'wordnet': 'Wordnet 3.0'
    }

    params = {
        'api_key': api_key,
        'limit': 1
    }
    json = requests.get(url, params=params).json()

    if json:
        return "\x02{}\x02: {} ({})".format(word,
            json[0]['text'],
            dictionaries[json[0]['sourceDictionary']])

    else:
        return "I could not find a definition for \x02{}\x02.".format(word)


@hook.command("wordusage", "wordexample", "usage")
def word_usage(text):
    """<word> -- Returns an example sentence showing the usage of <word>."""
    if not api_key:
        return "This command requires an API key from wordnik.com."
    word = text.split(' ')[0]
    url = BASE_URL + "word.json/{}/examples".format(word)
    params = {
        'api_key': api_key,
        'limit': 10
    }

    json = requests.get(url, params=params).json()
    if json:
        out = "\x02{}\x02: ".format(word)
        i = random.randint(0, len(json['examples']) - 1)
        out += "{} ".format(json['examples'][i]['text'])
        return out
    else:
        return "I could not find any usage examples for \x02{}\x02.".format(word)


@hook.command("pronounce", "sounditout")
def pronounce(text):
    """<word> -- Returns instructions on how to pronounce <word> with an audio example."""
    if not api_key:
        return "This command requires an API key from wordnik.com."
    word = text.split(' ')[0]
    url = BASE_URL + "word.json/{}/pronunciations".format(word)

    params = {
        'api_key': api_key,
        'limit': 5
    }
    json = requests.get(url, params=params).json()

    if json:
        out = "\x02{}\x02: ".format(word)
        out += " • ".join([i['raw'] for i in json])
    else:
        return "Sorry, I don't know how to pronounce \x02{}\x02.".format(word)

    url = BASE_URL + "word.json/{}/audio".format(word)

    params = {
        'api_key': api_key,
        'limit': 1,
        'useCanonical': 'false'
    }
    json = requests.get(url, params=params).json()

    if json:
        url = web.try_shorten(json[0]['fileUrl'])
        out += " - {}".format(url)

    return out


@hook.command()
def synonym(text):
    """<word> -- Returns a list of synonyms for <word>."""
    if not api_key:
        return "This command requires an API key from wordnik.com."
    word = text.split(' ')[0]
    url = BASE_URL + "word.json/{}/relatedWords".format(word)

    params = {
        'api_key': api_key,
        'relationshipTypes': 'synonym',
        'limitPerRelationshipType': 5
    }
    json = requests.get(url, params=params).json()

    if json:
        out = "\x02{}\x02: ".format(word)
        out += " • ".join(json[0]['words'])
        return out
    else:
        return "Sorry, I couldn't find any synonyms for \x02{}\x02.".format(word)


@hook.command()
def antonym(text):
    """<word> -- Returns a list of antonyms for <word>."""
    if not api_key:
        return "This command requires an API key from wordnik.com."
    word = text.split(' ')[0]
    url = BASE_URL + "word.json/{}/relatedWords".format(word)

    params = {
        'api_key': api_key,
        'relationshipTypes': 'antonym',
        'limitPerRelationshipType': 5,
        'useCanonical': 'false'
    }
    json = requests.get(url, params=params).json()

    if json:
        out = "\x02{}\x02: ".format(word)
        out += " • ".join(json[0]['words'])
        out = out[:-2]
        return out
    else:
        return "Sorry, I couldn't find any antonyms for \x02{}\x02.".format(word)


# word of the day
@hook.command("word", "wordoftheday", autohelp=False)
def wordoftheday(text, conn):
    """returns the word of the day. To see past word of the day enter use the format yyyy-MM-dd. The specified date must be after 2009-08-10."""
    if not api_key:
        return "This command requires an API key from wordnik.com."
    match = re.search(r'(\d\d\d\d-\d\d-\d\d)', text)
    date = ""
    if match:
        date = match.group(1)
    url = BASE_URL + "words.json/wordOfTheDay"
    if date:
        params = {
            'api_key': api_key,
            'date': date
        }
        day = date
    else:
        params = {
            'api_key': api_key,
        }
        day = "today"

    json = requests.get(url, params=params).json()

    if json:
        word = json['word']
        note = json['note']
        pos = json['definitions'][0]['partOfSpeech']
        definition = json['definitions'][0]['text']
        out = "The word for \x02{}\x02 is \x02{}\x02: ".format(day, word)
        out += "\x0305({})\x0305 ".format(pos)
        out += "\x0310{}\x0310 ".format(note)
        out += "\x02Definition:\x02 \x0303{}\x0303".format(definition)
        return out
    else:
        return "Sorry I couldn't find the word of the day, check out this awesome otter instead {}".format(
            "http://i.imgur.com/pkuWlWx.gif")


# random word
@hook.command("wordrandom", "randomword", autohelp=False)
def random_word(conn):
    """Grabs a random word from wordnik.com"""
    if not api_key:
        return "This command requires an API key from wordnik.com."
    url = BASE_URL + "words.json/randomWord"
    params = {
        'api_key': api_key,
        'hasDictionarydef': 'true',
        'vulgar': 'true'
    }
    json = requests.get(url, params=params).json()
    if json:
        word = json['word']
        return "Your random word is \x02{}\x02.".format(word)
    else:
        return "There was a problem contacting the wordnick.com API."
