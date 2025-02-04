__author__ = 'danilo@jaist.ac.jp'

from typing import List, Dict

from .sequence import Sequence
from .term import Term
from .token import Token


class Sentence(Sequence):
    """Description of a sentence: sequence of language tokens.

    Attributes:
    tokens (list of Token): Sequence of tokens composing the sentence, in reading order.
    terms (list of Term): [optional] Sequence of terms (morphemes -> phrases) composing the sentence, in reading order.
    annotations (dict): [optional] Sentence level annotations, identified by the dictionary key.
        Examples: sentence vector, inclusion status (in extractive summarization).
    """

    def __init__(self):
        super(Sentence, self).__init__()
        self.terms: List[Term] = []
        self._surface: str = None

    @property
    def surface(self) -> str:
        """Surface form of the sentence

        Default requires pre-processed form to be stored in the _surface property, but the implementation
        is dependent on language and tokenization method (e.g., white space, BPE, etc.)
        """
        if (self._surface is None):
            raise NotImplementedError

        return self._surface

    @surface.setter
    def surface(self, value):
        self._surface = value
