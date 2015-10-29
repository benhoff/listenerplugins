from pluginmanager import IPlugin

class ListenerPlugin(IPlugin):
    def __init__(self):
        super().__init__()
        self.matches = []
    
    def __call__(self, regex_command, message, *args, **kwargs):
        pass

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
