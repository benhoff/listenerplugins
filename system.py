import os
import re
import time
import platform
from datetime import timedelta

from util import hook


def convert_kilobytes(kilobytes):
    if kilobytes >= 1024:
        megabytes = kilobytes / 1024
        size = '%.2f MB' % megabytes
    else:
        size = '%.2f KB' % kilobytes
    return size


@hook.command(autohelp=False)
def system(inp):
    """system -- Retrieves information about the host system."""
    hostname = platform.node()
    os = platform.platform()
    python_imp = platform.python_implementation()
    python_ver = platform.python_version()
    architecture = '-'.join(platform.architecture())
    cpu = platform.machine()
    return "Hostname: \x02{}\x02, Operating System: \x02{}\x02, Python " \
           "Version: \x02{} {}\x02, Architecture: \x02{}\x02, CPU: \x02{}" \
           "\x02".format(hostname, os, python_imp, python_ver, architecture, cpu)


@hook.command(autohelp=False)
def memory(inp):
    """memory -- Displays the bot's current memory usage."""
    if os.name == "posix":
        # get process info
        status_file = open('/proc/self/status').read()
        s = dict(re.findall(r'^(\w+):\s*(.*)\s*$', status_file, re.M))
        # get the data we need and process it
        data = s['VmRSS'], s['VmSize'], s['VmPeak'], s['VmStk'], s['VmData']
        data = [float(i.replace(' kB', '')) for i in data]
        strings = [convert_kilobytes(i) for i in data]
        # prepare the output
        out = "Threads: \x02{}\x02, Real Memory: \x02{}\x02, Allocated Memory: \x02{}\x02, Peak " \
              "Allocated Memory: \x02{}\x02, Stack Size: \x02{}\x02, Heap " \
              "Size: \x02{}\x02".format(s['Threads'], strings[0], strings[1], strings[2],
              strings[3], strings[4])
        # return output
        return out

    elif os.name == "nt":
        cmd = 'tasklist /FI "PID eq %s" /FO CSV /NH' % os.getpid()
        out = os.popen(cmd).read()
        memory = 0
        for amount in re.findall(r'([,0-9]+) K', out):
            memory += float(amount.replace(',', ''))
        memory = convert_kilobytes(memory)
        return "Memory Usage: \x02{}\x02".format(memory)

    else:
        return "Sorry, this command is not supported on your OS."


@hook.command(autohelp=False)
def uptime(inp, bot=None):
    """uptime -- Shows the bot's uptime."""
    uptime_raw = round(time.time() - bot.start_time)
    uptime = timedelta(seconds=uptime_raw)
    return "Uptime: \x02{}\x02".format(uptime)


@hook.command(autohelp=False)
def pid(inp):
    """pid -- Prints the bot's PID."""
    return "PID: \x02{}\x02".format(os.getpid())
