__author__ = 'Danilo S. Carvalho <danilo.carvalho@manchester.ac.uk>'

from enum import Enum
from saf.data_model.document import Document
from saf.data_model.sentence import Sentence
from saf.data_model.token import Token
from saf.constants import annotation
from .importer import Importer

class MorphoDBImporter(Importer):
    DECOMP_PASS_LIMIT = 4
    def __init__(self):
        """Importer class for converting a MorphoDB document into an Annotable document."""
        super(MorphoDBImporter, self).__init__(None, None)

    def import_document(self, document: dict, chars: bool = False) -> Document:
        """Imports a MorphoDB document

        Args:
            document (dict): MorphoDB document to be imported as a SAF document.

        Returns:
            Document: The imported document
        """
        for entry in document:
            total_decomp = False
            decomp = None
            tmp_morphemes = list(document[entry]["morphemes"]["seq"])
            passes = 0

            while (not total_decomp):
                total_decomp = True
                decomp = list()
                for morpheme in tmp_morphemes:
                    if (morpheme in document and passes < MorphoDBImporter.DECOMP_PASS_LIMIT):
                        decomp.extend(document[morpheme]["morphemes"]["seq"])
                        total_decomp = False
                    else:
                        decomp.append(morpheme)
                    passes += 1

                tmp_morphemes = list(decomp)

            document[entry]["morphemes"]["seq"] = decomp

        doc = Document()
        for entry in document:
            sentence = Sentence()
            if (not chars):
                for morpheme in document[entry]["morphemes"]["seq"]:
                    token = Token()
                    token.surface = morpheme
                    sentence.tokens.append(token)
            else:
                for char in list(" ".join(document[entry]["morphemes"]["seq"])):
                    token = Token()
                    token.surface = char
                    sentence.tokens.append(token)

            sentence.annotations[annotation.MORPH_TYPE] = document[entry]["morphemes"]["type"]
            doc.sentences.append(sentence)

        return doc
