import yapsy

class ListenerPlugin(yapsy.IPlugin):
    def __init__(self, function=None, config_source=None):
        super(ListenerPlugin, self).__init__()
        self.config_source = config_source
        self.matches = []
        self.function = function
    
    def call(self, message, done=None, *args, **kwargs):
        if command in self.matches:
            # TODO: add in authentication here
            result = function(argument, *args, **kwargs)
            if isinstance(done, types.FunctionType):
                done()
            done = True
            return result, done

from .amazon import Amazon
from .books import Books
from .brainfuck import Brainfuck
from .chatbot import ChatBot
from .cryptocurrency import Cryptocurrency
from .cypher import Cypher
from .dramatica import Drama
from .etymology import Etymology
from .feeds import Feeds
from .issafe import IsSafe
from .wikipedia import Wikipedia
