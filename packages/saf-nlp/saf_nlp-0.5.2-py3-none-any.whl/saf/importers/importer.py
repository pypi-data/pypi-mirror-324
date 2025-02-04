__author__ = 'Danilo S. Carvalho <danilo@jaist.ac.jp>, Vu Duc Tran <vu.tran@jaist.ac.jp>'

from abc import ABC
from abc import abstractmethod
from saf import Document


class Importer(ABC):
    """Provides a facility for importing documents from different sources into SAFs document model.

    A basic implementation (saf.importers.PlainTextImporter) tokenizes a plain text document into sentences using
    sentence_tokenizer and words in a sentence using word_tokenizer.

    Args:
        sentence_tokenizer: tokenizer to separate sentences in a document.
            Should be a callable object tokenizer(txt: str) -> List[str]
            Example: nltk.tokenize.sent_tokenize
        word_tokenizer: tokenizer to separate words in a sentence.
            Should be a callable object tokenizer(txt: str) -> List[str]
            Example: nltk.tokenize.word_tokenize

    """
    def __init__(self, sentence_tokenizer, word_tokenizer):
        self.sent_tokenizer = sentence_tokenizer
        self.word_tokenizer = word_tokenizer


    @abstractmethod
    def import_document(self, document) -> Document:
        """Imports a plain text document

        Args:
            document (str): plain text to be imported as a document.

        Returns:
        Document: The imported document
        """
        raise NotImplementedError()


