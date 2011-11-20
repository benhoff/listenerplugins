import re
import random

from util import hook


@hook.command
def choose(inp):
    ".choose <choice1>, <choice2>, ... <choicen> -- makes a decision"

    c = re.findall(r'([^,]+)', inp)
    if len(c) == 1:
        c = re.findall(r'(\S+)', inp)
        if len(c) == 1:
            return 'the decision is up to you'

    return random.choice(c).strip()
