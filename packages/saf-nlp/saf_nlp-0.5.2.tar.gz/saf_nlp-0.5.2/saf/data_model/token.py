__author__ = 'Danilo S. Carvalho <danilo@jaist.ac.jp>, Vu Duc Tran <vu.tran@jaist.ac.jp>'

from typing import Dict

from .annotable import Annotable


class Token(Annotable):
    """Description of a token.

    Attributes:
    surface (unicode): Surface form of the token.
    annotations (dict): [optional] Token level annotations, identified by the dictionary key.
        Examples: word vector, POS tag.
    """

    def __init__(self):
        super(Token, self).__init__()
        self.surface: str = ""
