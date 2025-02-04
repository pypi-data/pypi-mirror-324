__author__ = 'danilo@jaist.ac.jp'

from typing import List, Dict

from .annotable import Annotable
from .term import Term
from .token import Token


class Sequence(Annotable):
    """Description of a sequence.

    Attributes:
    tokens (list of Token): Sequence of tokens composing the sequence, in reading order.
    annotations (dict): [optional] Sequence level annotations, identified by the dictionary key.
        Examples: sequence type, batch / sample identifier, sequence-level vectors.
    """

    def __init__(self):
        super(Sequence, self).__init__()
        self.tokens: List[Token] = []
