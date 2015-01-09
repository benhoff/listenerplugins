from cloudbot.util import cleverbot
from cloudbot import hook


@hook.command
def ask(text):
    """ <question> -- Asks Cleverbot <question> """
    session = cleverbot.Session()
    data = session.ask(text)
    return data
