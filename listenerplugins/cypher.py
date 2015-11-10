"""
cypher.py

Ciphers and deciphers strings.

Created By:
    - Tom <https://github.com/instanceoftom>

Modified By:
    - Fletcher Boyd <https://github.com/thenoodle68>
    - Dabo Ross <https://github.com/daboross>
    - Luke Rogers <https://github.com/lukeroge>

License:
    GPL v3
"""
import types
import base64
import binascii
import re
from . import ListenerPlugin

class Cypher(ListenerPlugin):
    def __init__(self):
        super().__init__()
        self._cypher_matches = [re.compile('cypher'), re.compile('cipher')]
        self._decypher_matches = [re.compile('decypher'), re.compile('decipher')]

        self.matches = []
        self.matches.extend(self._cypher_matches)
        self.matches.extend(self._decypher_matches)
    
    def __call__(self, regex_command, string_argument):
        if regex_command in self._cypher_matches:
            result = cypher(string_argument)
        elif regex_command in self._decypher_matches:
            result = decypher(string_argument)
        return result

def encode(password, text):
    """
    :type password: str
    :type text: str
    """
    enc = []
    for i in range(len(text)):
        key_c = password[i % len(password)]
        enc_c = chr((ord(text[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()


def decode(password, encoded):
    """
    :type password: str
    :type encoded: str
    """
    dec = []
    try:
        encoded_bytes = base64.urlsafe_b64decode(encoded.encode()).decode()
    except binascii.Error:
        return "Invalid input '{}'".format(encoded)
    for i in range(len(encoded_bytes)):
        key_c = password[i % len(password)]
        dec_c = chr((256 + ord(encoded_bytes[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)


def cypher(text):
    """<pass> <string> -- cyphers <string> with <password>"""
    split = text.split(None, 1)
    if len(split) < 2:
        return cypher.__doc__
    password = split[0]
    plaintext = split[1]
    return encode(password, plaintext)


def decypher(text):
    """<pass> <string> - decyphers <string> with <password>"""
    split = text.split(None, 1)
    if len(split) < 2:
        return decypher.__doc__
    password = split[0]
    encoded = split[1]
    return decode(password, encoded)
