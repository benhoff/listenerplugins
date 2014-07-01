import random
import re
import time

from cloudbot import hook


def format_quote(q, num, n_quotes):
    """Returns a formatted string of a quote"""
    ctime, nick, msg = q
    return "[{}/{}] <{}> {}".format(num, n_quotes,
                                    nick, msg)


def create_table_if_not_exists(db):
    """Creates an empty quote table if one does not already exist"""
    db.execute("create table if not exists quote"
               "(chan, nick, add_nick, msg, time real, deleted default 0, "
               "primary key (chan, nick, msg))")
    db.commit()


def add_quote(db, chan, nick, add_nick, msg):
    """Adds a quote to a nick, returns message string"""
    try:
        db.execute('''INSERT OR FAIL INTO quote
                      (chan, nick, add_nick, msg, time)
                      VALUES(?,?,?,?,?)''',
                   (chan, nick, add_nick, msg, time.time()))
        db.commit()
    except db.IntegrityError:
        return "Message already stored, doing nothing."
    return "Quote added."


def del_quote(db, chan, nick, add_nick, msg):
    """Deletes a quote from a nick"""
    db.execute('''UPDATE quote SET deleted = 1 WHERE
                  chan=? AND lower(nick)=lower(?) AND msg=msg''')
    db.commit()


def get_quote_num(num, count, name):
    """Returns the quote number to fetch from the DB"""
    if num:  # Make sure num is a number if it isn't false
        num = int(num)
    if count == 0:  # Error on no quotes
        raise Exception("No quotes found for {}.".format(name))
    if num and num < 0:  # Count back if possible
        num = count + num + 1 if num + count > -1 else count + 1
    if num and num > count:  # If there are not enough quotes, raise an error
        raise Exception("I only have {} quote{} for {}.".format(count, ('s', '')[count == 1], name))
    if num and num == 0:  # If the number is zero, set it to one
        num = 1
    if not num:  # If a number is not given, select a random one
        num = random.randint(1, count)
    return num


def get_quote_by_nick(db, nick, num=False):
    """Returns a formatted quote from a nick, random or selected by number"""
    count = db.execute('''SELECT COUNT(*) FROM quote WHERE deleted != 1
                          AND lower(nick) = lower(?)''', [nick]).fetchall()[0][0]

    try:
        num = get_quote_num(num, count, nick)
    except Exception as error_message:
        return error_message

    quote = db.execute('''SELECT time, nick, msg
                          FROM quote
                          WHERE deleted != 1
                          AND lower(nick) = lower(?)
                          ORDER BY time
                          LIMIT ?, 1''', (nick, (num - 1))).fetchall()[0]
    return format_quote(quote, num, count)


def get_quote_by_nick_chan(db, chan, nick, num=False):
    """Returns a formatted quote from a nick in a channel, random or selected by number"""
    count = db.execute('''SELECT COUNT(*)
                          FROM quote
                          WHERE deleted != 1
                          AND chan = ?
                          AND lower(nick) = lower(?)''', (chan, nick)).fetchall()[0][0]

    try:
        num = get_quote_num(num, count, nick)
    except Exception as error_message:
        return error_message

    quote = db.execute('''SELECT time, nick, msg
                          FROM quote
                          WHERE deleted != 1
                          AND chan = ?
                          AND lower(nick) = lower(?)
                          ORDER BY time
                          LIMIT ?, 1''', (chan, nick, (num - 1))).fetchall()[0]
    return format_quote(quote, num, count)


def get_quote_by_chan(db, chan, num=False):
    """Returns a formatted quote from a channel, random or selected by number"""
    count = db.execute('''SELECT COUNT(*)
                          FROM quote
                          WHERE deleted != 1
                          AND chan = ?''', (chan,)).fetchall()[0][0]

    try:
        num = get_quote_num(num, count, chan)
    except Exception as error_message:
        return error_message

    quote = db.execute('''SELECT time, nick, msg
                          FROM quote
                          WHERE deleted != 1
                          AND chan = ?
                          ORDER BY time
                          LIMIT ?, 1''', (chan, (num - 1))).fetchall()[0]
    return format_quote(quote, num, count)


@hook.command('q')
@hook.command()
def quote(text, nick='', chan='', db=None, notice=None):
    """[#chan] [nick] [#n] OR add <nick> <message> - gets the [#n]th quote by <nick> (defaulting to random) OR adds <message> as a quote for <nick> in the caller's channel"""
    create_table_if_not_exists(db)

    add = re.match(r"add[^\w@]+(\S+?)>?\s+(.*)", text, re.I)
    retrieve = re.match(r"(\S+)(?:\s+#?(-?\d+))?$", text)
    retrieve_chan = re.match(r"(#\S+)\s+(\S+)(?:\s+#?(-?\d+))?$", text)

    if add:
        quoted_nick, msg = add.groups()
        notice(add_quote(db, chan, quoted_nick, nick, msg))
        return
    elif retrieve:
        select, num = retrieve.groups()
        by_chan = True if select.startswith('#') else False
        if by_chan:
            return get_quote_by_chan(db, select, num)
        else:
            return get_quote_by_nick(db, select, num)
    elif retrieve_chan:
        chan, nick, num = retrieve_chan.groups()
        return get_quote_by_nick_chan(db, chan, nick, num)

    notice(quote.__doc__)
