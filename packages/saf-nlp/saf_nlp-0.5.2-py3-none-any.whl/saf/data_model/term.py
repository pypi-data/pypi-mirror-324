__author__ = 'Danilo S. Carvalho <danilo@jaist.ac.jp>, Vu Duc Tran <vu.tran@jaist.ac.jp>'

from typing import List, Dict

from .annotable import Annotable
from .token import Token


class Term(Annotable):
    """Description of a term.

    Attributes:
    surface (unicode): Surface form of the term.
    tokens (list of Token): [optional] Sequence of tokens composing this term.
    annotations (dict): [optional] Token level annotations, identified by the dictionary key.
        Examples: word vector, POS tag.
    """

    def __init__(self):
        super(Term, self).__init__()
        self.surface: str = ""
        self.tokens: List[Token] = []
