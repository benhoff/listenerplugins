# Plugin made by iloveportalz0r, TheNoodle, Lukeroge and neersighted
from util import hook
import os
import sys
import subprocess
import time
import re


@hook.command(autohelp=False)
def admins(inp, bot=None):
    ".admins -- Lists the bot's admins."
    admins = bot.config["admins"]
    return ", ".join(admins)


@hook.command(autohelp=False)
def channels(inp, conn=None):
    ".channels -- Lists the channels that the bot is in."
    return "I am in these channels: %s" % ", ".join(conn.channels)


@hook.command(autohelp=False, adminonly=True)
def stop(inp, nick=None, conn=None):
    ".stop [reason] -- Kills the bot with [reason] as its quit message."
    if inp:
        conn.cmd("QUIT", ["Killed by %s (%s)" % (nick, inp)])
    else:
        conn.cmd("QUIT", ["Killed by %s." % nick])
    time.sleep(5)
    os.execl(["./cloudbot", "stop"])

@hook.command(autohelp=False, adminonly=True)
def restart(inp, nick=None, conn=None):
    ".restart [reason] -- Restarts the bot with [reason] as its quit message."
    if inp:
        conn.cmd("QUIT", ["Restarted by %s (%s)" % (nick, inp)])
    else:
        conn.cmd("QUIT", ["Restarted by %s." % nick])
    time.sleep(5)
    os.execl("./cloudbot", "restart")


@hook.command(autohelp=False, adminonly=True)
def clearlogs(inp, input=None):
    ".clearlogs -- Clears the bots log(s)."
    subprocess.call(["./cloudbot", "clear"])


@hook.command(adminonly=True)
def join(inp, conn=None, notice=None):
    ".join <channel> -- Joins <channel>."
    notice("Attempting to join %s..." % inp)
    conn.join(inp)


@hook.command(adminonly=True)
def cycle(inp, conn=None, notice=None):
    ".cycle <channel> -- Cycles <channel>."
    notice("Attempting to cycle %s..." % inp)
    conn.part(inp)
    conn.join(inp)


@hook.command(adminonly=True)
def part(inp, conn=None, notice=None):
    ".part <channel> -- Leaves <channel>."
    notice("Attempting to part from %s..." % inp)
    conn.part(inp)


@hook.command(adminonly=True)
def nick(inp, input=None, notice=None, conn=None):
    ".nick <nick> -- Changes the bots nickname to <nick>."
    if not re.match("^[A-Za-z0-9_|.-\]\[]*$", inp.lower()):
        notice("Invalid username!")
        return
    notice("Attempting to change nick to \"%s\"..." % inp)
    conn.set_nick(inp)


@hook.command(adminonly=True)
def raw(inp, conn=None, notice=None):
    ".raw <command> -- Sends a RAW IRC command."
    notice("Raw command sent.")
    conn.send(inp)


@hook.command(adminonly=True)
def kick(inp, chan=None, conn=None, notice=None):
    ".kick [channel] <user> [reason] -- Makes the bot kick <user> in [channel] "\
    "If [channel] is blank the bot will kick the <user> in "\
    "the channel the command was used in."
    split = inp.split(" ")
    if split[0][0] == "#":
        chan = split[0]
        user = split[1]
        out = "KICK %s %s" % (chan, user)
        if len(split) > 2:
            reason = ""
            for x in split[2:]:
                reason = reason + x + " "
            reason = reason[:-1]
            out = out + " :" + reason
    else:
        user = split[0]
        out = "KICK %s %s" % (chan, split[0])
        if len(split) > 1:
            reason = ""
            for x in split[1:]:
                reason = reason + x + " "
            reason = reason[:-1]
            out = out + " :" + reason

    notice("Attempting to kick %s from %s..." % (user, chan))
    conn.send(out)


@hook.command(adminonly=True)
def say(inp, conn=None, chan=None, notice=None):
    ".say [channel] <message> -- Makes the bot say <message> in [channel]. "\
    "If [channel] is blank the bot will say the <message> in "\
    "the channel the command was used in."
    split = inp.split(" ")
    if split[0][0] == "#":
        message = ""
        for x in split[1:]:
            message = message + x + " "
        message = message[:-1]
        out = "PRIVMSG %s :%s" % (split[0], message)
    else:
        message = ""
        for x in split[0:]:
            message = message + x + " "
        message = message[:-1]
        out = "PRIVMSG %s :%s" % (chan, message)
    conn.send(out)


@hook.command("act", adminonly=True)
@hook.command(adminonly=True)
def me(inp, conn=None, chan=None, notice=None):
    ".me [channel] <action> -- Makes the bot act out <action> in [channel] "\
    "If [channel] is blank the bot will act the <action> in "\
    "the channel the command was used in."
    split = inp.split(" ")
    if split[0][0] == "#":
        message = ""
        for x in split[1:]:
            message = message + x + " "
        message = message[:-1]
        out = "PRIVMSG %s :\x01ACTION %s\x01" % (split[0], message)
    else:
        message = ""
        for x in split[0:]:
            message = message + x + " "
        message = message[:-1]
        out = "PRIVMSG %s :\x01ACTION %s\x01" % (chan, message)
    conn.send(out)


@hook.command(adminonly=True)
def topic(inp, conn=None, chan=None, notice=None):
    ".topic [channel] <topic> -- Change the topic of a channel."
    split = inp.split(" ")
    if split[0][0] == "#":
        out = "PRIVMSG %s :%s" % (split[0], message)
    else:
        out = "TOPIC %s :%s" % (input.chan, message)
    input.conn.send(out)
