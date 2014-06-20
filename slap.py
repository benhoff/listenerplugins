import json

from cloudbot import hook
from cloudbot.util import textgen


def get_generator(_json, variables):
    data = json.loads(_json)
    return textgen.TextGenerator(data["templates"],
                                 data["parts"], variables=variables)


@hook.command()
def slap(text, action, nick, conn, notice):
    """slap <user> -- Makes the bot slap <user>."""
    target = text.strip()

    if " " in target:
        notice("Invalid username!")
        return

    # if the user is trying to make the bot slap itself, slap them
    if target.lower() == conn.nick.lower() or target.lower() == "itself":
        target = nick

    variables = {
        "user": target
    }

    with open("./data/slaps.json") as f:
        generator = get_generator(f.read(), variables)

    # act out the message
    action(generator.generate_string())
