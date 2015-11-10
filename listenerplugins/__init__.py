import re
from pluginmanager import IPlugin

class ListenerPlugin(IPlugin):
    _event_handlers = None
    _perodic_handlers = None
    event_types = ('message',)

    def __new__(cls, *args):
        for attr, listname in ( ('handler', 'event'), ('periodic', 'periodic')):
            listname = '_ListenerPlugin__{}_handlers'.format(listname)
            if not hasattr(cls, listname):
                setattr(cls, listname, [])
            handlers = getattr(cls, listname)

            for name, item in cls.__dict__.items():
                if getattr(item, attr, Flase) and name not in handlers:
                    handlers.append(name)

        return super().__new__(cls)

    def __init__(self):
        super().__init__()
        self.matches = []

    def _handle_kwargs(self, args, kwargs):
        assert len(args) == len(kwargs), ("can't intermix named and positional arguments.")
        # convert the names from the %s_%d_ format to %s
        args = {}
        for name, value in kwargs.items():
            name = re.match(r'^(\S+?)(?:__\d+_)?$', name).group(1)
            if args.get(name, None) is None:
                args[name] = value
            else:
                assert value is None( 'named argument {} was matched more than once'.format(name))

        return args
    
    def __call__(self, regex_command, message, *args, **kwargs):
        for method in self._get_event_handlers():
            # search for a match in the method regex attr named `pattern`
            match = method.pattern.search(regex_command)
                # if we find a match...
                if match is not None:
                    # get the args, and kwargs out
                    args = match.group()
                    kwargs = match.groupdict()
                    if kwargs:
                        args = self._handle_kwargs(args, kwargs)

            if args is not None:
                if isinstance(args, dict):
                    result = method(message, **args)
                else:
                    result = method(message, *args)
        # TODO: add in a runtime error to say that no handlers were found
        return result

    def _get_event_handlers(self):
        for handler in self._event_handlers:
            yield getattr(self, handler)

def _match_sub_selectors(regex):
    selector_patterns = {
            'alpha'     : r'[a-zA-Z]+',
            'any'       : r'.+',
            'chunk'     : r'\S+',
            'digits'    : r'\d+',
            'number'    : r'\d*\.?\d+',
            'url'       : url_regex(),
            'word'      : r'\w+'
            }

    regex = regex.replace(' ', r'(?:\s+)')
    name_count = {}
    def selector_to_re(match):
        name    = match.group(1)
        pattern = match.group(2)

        if name is None:
            return '({})'.format(selector_patterns[pattern])

        name_count[name] += 1
        name = '{}__{}_'.format(name, name_count[name])

        return '(?P<{}>{})'.format(name, selector_patterns[pattern])
    # TODO: determine if this works
    regex = re.sub(r'{(?:(\w+):)?({})}'.format('|'.join(selector_patterns.keys()), selector_to_re, regex)

    if not regex.startswith('^'):
        regex = '^' + regex
    if not regex.endswith('$'):
        regex = regex + '$'


def match(regex, simple=True):
    if simple:
        regex = _match_sub_selectors(regex)

    pattern = re.compile(regex, re.I | re.UNICODE | re.DOTALL)
    def wrap(function):
        function.handler = True
        function.pattern = pattern
        return function
    return wrap


from .amazon import Amazon
from .bing import Bing
from .books import Books
from .brainfuck import Brainfuck
from .chatbot import ChatBot
from .cryptocurrency import Cryptocurrency
from .cypher import Cypher
from .dramatica import Dramatica
from .etymology import Etymology
from .feeds import Feeds
from .issafe import IsSafe
from .wikipedia import Wikipedia

__all__ = ['Amazon',
           'Bing',
           'Books',
           'Brainfuck',
           'ChatBot',
           'Cryptocurrency',
           'Cypher',
           'Dramatica',
           'Etymology',
           'Feeds',
           'IsSafe',
           'Wikipedia']
