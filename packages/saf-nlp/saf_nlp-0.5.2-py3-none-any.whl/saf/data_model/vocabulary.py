__author__ = 'danilo.carvalho@manchester.ac.uk'

from typing import List, Dict, Iterable, Union, Hashable
from collections import Counter

from .annotable import Annotable


def format_annotation(label: Hashable, lowercase: bool) -> Hashable:
    if (lowercase and isinstance(label, str)):
        label = label.lower()

    return label



class Vocabulary:
    """Represents the vocabulary comprising the symbols of a collection of Annotables

        Each token or annotation in the collection is associated to a symbol (its surface form).
        Each symbol is mapped to an index, which can be used for vectorizing the annotables.

        Args:
            data (list of Annotable): list of annotables for which the vocabulary will be extracted.
            source (str): if specified, will use annotation symbols for the given tag, instead of token surface forms.
                          Only hashable annotations are supported.
            maxlen (int): maximum size of the vocabulary. If exceeded, the most frequent symbols are selected.
        """
    def __init__(self, data: Iterable[Annotable] = None, source: str = "_token", maxlen: int = None, lowercase: bool = True):
        self.source = source
        self.lowercase = lowercase
        if (data):
            tokens = list()
            labels = list()
            for annotable in data:
                if (hasattr(annotable, "sentences")):
                    for sent in annotable.sentences:
                        tokens.extend(sent.tokens)
                        if (source in sent.annotations):
                            labels.append(sent.annotations[source])
                elif (hasattr(annotable, "tokens")):
                    if (source in annotable.annotations):
                        labels.append(annotable.annotations[source])
                    tokens.extend(annotable.tokens)

            for tok in tokens:
                if (source in tok.annotations):
                    labels.append(tok.annotations[source])

            if (source == "_token"):
                self.freqs: Counter[str] = Counter([tok.surface.lower() if lowercase else tok.surface for tok in tokens])
            else:
                self.freqs: Counter[Hashable] = Counter([
                    format_annotation(label, lowercase) for label in labels
                    if (label is not None)
                ])

            self._vocab: Dict[Hashable, int] = {symbol: i for i, symbol in enumerate(sorted(self.freqs.keys()))}
            self._rev_vocab: Dict[int, Hashable] = {i: symbol for symbol, i in self._vocab.items()}

            if (maxlen):
                excl = set(self.freqs.keys()) - set([symbol for symbol, freq in self.freqs.most_common(maxlen)])
                self.del_symbols(list(excl))

    def __len__(self):
        return len(self._vocab)

    @property
    def symbols(self) -> Iterable[str]:
        return self._vocab.keys()

    def add_symbols(self, symbols: List[str]):
        for symbol in symbols:
            if (symbol not in self._vocab):
                self._vocab[symbol] = len(self._vocab)
        self._rev_vocab = {i: symbol for symbol, i in self._vocab.items()}

    def del_symbols(self, symbols: List[str]):
        for symbol in symbols:
            idx = self.get_index(symbol)
            del self._vocab[symbol]
            del self.freqs[symbol]
            del self._rev_vocab[idx]

        self._vocab = {s: i for i, s in enumerate(self._vocab.keys())}
        self._rev_vocab = {i: symbol for symbol, i in self._vocab.items()}

    def get_index(self, symbol: str) -> int:
        return self._vocab[symbol]

    def get_symbol(self, index: int) -> str:
        return self._rev_vocab[index]

    def to_indices(self, data: Iterable[Annotable], default: int = -1, padding: int = 0,
                   pad_symbol: str = None, start_symbol: str = None, end_symbol: str = None) -> Union[List[List[int]], List[List[List[int]]]]:
        indices = list()

        if (padding < 0):
            for annotable in data:
                if (hasattr(annotable, "sentences")):
                    maxlen = max([len(sent.tokens) for sent in annotable.sentences])
                    padding = maxlen if (padding < maxlen) else padding
                elif (hasattr(annotable, "tokens")):
                    padding = len(annotable.tokens) if (padding < len(annotable.tokens)) else padding

            if (start_symbol):
                padding += 1
            if (end_symbol):
                padding += 1

        for annotable in data:
            if (hasattr(annotable, "sentences")):
                indices.append(list())
                for sent in annotable.sentences:
                    if (self.source in sent.annotations):
                        annot = sent.annotations[self.source].lower() if self.lowercase else sent.annotations[self.source]
                        indices[-1].append(self._vocab.get(annot, default))
                    else:
                        if (self.source == "_token"):
                            indices[-1].append([self._vocab.get(tok.surface.lower() if self.lowercase else tok.surface, default)
                                                for tok in sent.tokens])
                        else:
                            indices[-1].append([self._vocab.get(tok.annotations[self.source].lower()
                                                                if self.lowercase
                                                                else tok.annotations[self.source], default)
                                                for tok in sent.tokens])

                        if (start_symbol is not None):
                            indices[-1][-1].insert(0, self._vocab.get(start_symbol, default))
                        if (end_symbol is not None):
                            indices[-1][-1].append(self._vocab.get(end_symbol, default))
                        if (padding and len(indices[-1][-1]) < padding):
                            indices[-1][-1].extend([self._vocab.get(pad_symbol, default)] * (padding - len(indices[-1][-1])))
            elif (hasattr(annotable, "tokens")):
                if (self.source in annotable.annotations):
                    indices.append(self._vocab.get(annotable.annotations[self.source], default))
                else:
                    if (self.source == "_token"):
                        indices.append([self._vocab.get(tok.surface.lower() if self.lowercase else tok.surface, default)
                                        for tok in annotable.tokens])
                    else:
                        indices.append([self._vocab.get(tok.annotations[self.source].lower()
                                                        if self.lowercase
                                                        else tok.annotations[self.source], default)
                                        for tok in annotable.tokens])

                    if (start_symbol is not None):
                        indices[-1].insert(0, self._vocab.get(start_symbol, default))
                    if (end_symbol is not None):
                        indices[-1].append(self._vocab.get(end_symbol, default))
                    if (padding and len(indices[-1]) < padding):
                        indices[-1].extend([self._vocab.get(pad_symbol, default)] * (padding - len(indices[-1])))

        return indices

