import json
from util import hook
from fnmatch import fnmatch


@hook.sieve
def ignoresieve(bot, input, func, type, args):
    """ blocks input from ignored channels/hosts """
    ignorelist = bot.config["plugins"]["ignore"]["ignored"]
    mask = input.mask.lower()

    # don't block input to event hooks
    if type == "event":
        return input

    if ignorelist:
        for pattern in ignorelist:
            if fnmatch(mask, pattern):
                if input.command == "PRIVMSG" and input.lastparam[1:] == "unignore":
                    return input
                else:
                    return None
            elif pattern.startswith("#") and pattern in ignorelist:
                if input.command == "PRIVMSG" and input.lastparam[1:] == "unignore":
                    return input
                else:
                    return None

    return input


@hook.command(autohelp=False)
def ignored(inp, notice=None, bot=None):
    "ignored -- Lists ignored channels/users."
    ignorelist = bot.config["plugins"]["ignore"]["ignored"]
    if ignorelist:
        notice("Ignored channels/users are: %s" % ", ".join(ignorelist))
    else:
        notice("No masks are currently ignored.")
    return


@hook.command(permissions=["ignore"])
def ignore(inp, notice=None, bot=None, config=None):
    "ignore <channel|nick|host> -- Makes the bot ignore <channel|user>."
    target = inp.lower()
    ignorelist = bot.config["plugins"]["ignore"]["ignored"]
    if target in ignorelist:
        notice("%s is already ignored." % target)
    else:
        notice("%s has been ignored." % target)
        ignorelist.append(target)
        ignorelist.sort()
        json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)
    return


@hook.command(permissions=["ignore"])
def unignore(inp, notice=None, bot=None, config=None):
    "unignore <channel|user> -- Makes the bot listen to"\
    " <channel|user>."
    target = inp.lower()
    ignorelist = bot.config["plugins"]["ignore"]["ignored"]
    if target in ignorelist:
        notice("%s has been unignored." % target)
        ignorelist.remove(target)
        ignorelist.sort()
        json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)
    else:
        notice("%s is not ignored." % target)
    return
