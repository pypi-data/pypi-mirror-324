# Simple Annotation Framework (SAF)

The Simple Annotation Framework (SAF) is a lightweight Python library for annotating text data. It provides a simple and flexible way to create, manipulate, and export annotations in various formats.

![](https://github.com/dscarvalho/saf/raw/master/saf_diag.svg)

SAF is built upon a minimalistic data model, accessible through its API. This data model is flexible enough to be used by most types of linguistic annotation, and can store other types of data associated to the language items (e.g., statistics, data sources, schemas, etc.)

![](https://github.com/dscarvalho/saf/raw/master/saf_class_diag.svg)

## Installation

To install SAF, you can use pip:

```bash
pip install saf
```

## Usage

### Importing Text Data

SAF provides importers for different annotated text data formats, including plain text, ConLL and WebAnno.

#### Plain text

```python
from saf.importers.plain import PlainTextImporter
from saf.constants import annotation
from nltk.tokenize import sent_tokenize, word_tokenize

plain_doc = """
They buy and sell books.
I have no clue.
"""

# Import document
plain_importer = PlainTextImporter(sent_tokenize, word_tokenize)
doc = plain_importer.import_document(plain_doc)

print(len(doc.sentences))  # Number of sentences in the document.
print([tok.surface for tok in doc.sentences[1].tokens])  # Listing tokens for the second sentence in the document.
```

#### ConLL

```python
from saf import Document
from saf.constants import annotation
from saf.importers.conll import CoNLLImporter

conll_doc = """
# sent_id = 1
# text = They buy and sell books.
1   They     they    PRON    PRP    Case=Nom|Number=Plur               2   nsubj   2:nsubj|4:nsubj   _
2   buy      buy     VERB    VBP    Number=Plur|Person=3|Tense=Pres    0   root    0:root            _
3   and      and     CCONJ   CC     _                                  4   cc      4:cc              _
4   sell     sell    VERB    VBP    Number=Plur|Person=3|Tense=Pres    2   conj    0:root|2:conj     _
5   books    book    NOUN    NNS    Number=Plur                        2   obj     2:obj|4:obj       SpaceAfter=No
6   .        .       PUNCT   .      _                                  2   punct   2:punct           _

# sent_id = 2
# text = I have no clue.
1   I       I       PRON    PRP   Case=Nom|Number=Sing|Person=1     2   nsubj   _   _
2   have    have    VERB    VBP   Number=Sing|Person=1|Tense=Pres   0   root    _   _
3   no      no      DET     DT    PronType=Neg                      4   det     _   _
4   clue    clue    NOUN    NN    Number=Sing                       2   obj     _   SpaceAfter=No
5   .       .       PUNCT   .     _                                 2   punct   _   _
"""

conll_importer = CoNLLImporter(field_list=[annotation.LEMMA, annotation.UPOS, annotation.POS])
doc = conll_importer.import_document(conll_doc)

print(len(doc.sentences))  # Number of sentences in the document.
print(doc.sentences[0].surface)  # Surface form of the first sentence in the document.
print([tok.annotations[annotation.UPOS] for tok in doc.sentences[1].tokens]) # All universal POS tags from the second sentence.
```


### Annotating Text Data

The [saf_datasets](https://github.com/neuro-symbolic-ai/saf_datasets) library provides various annotated NLP datasets and facilities for automated annotation of your own data.   



### Exporting Annotated Text Data

SAF provides formatters for different annotation formats:


#### ConLL

```python
from saf.importers.plain import PlainTextImporter
from saf.constants import annotation
from nltk.tokenize import sent_tokenize, word_tokenize
from saf.formatters.conll import CoNLLFormatter

plain_doc = """
They buy and sell books.
I have no clue.
"""

# Import document
plain_importer = PlainTextImporter(sent_tokenize, word_tokenize)
doc = plain_importer.import_document(plain_doc)

# Annotate tokens
for sent in doc.sentences:
    for i, token in enumerate(sent.tokens):
        token.annotations[annotation.ID] = str(i)

conll_formatter = CoNLLFormatter(field_list=[annotation.ID])
conll_formatted_doc = conll_formatter.dumps(doc)

print(conll_formatted_doc)
```

### Working with vocabularies

Vocabulary objects can be used to quickly index and manage symbols in documents or sentence collections.  They facilitate vectorization for language model training, specially with label supervision. 

```python
from saf import Document
from saf.constants import annotation
from saf.importers.conll import CoNLLImporter
from saf import Vocabulary

conll_doc = """
# sent_id = 1
# text = They buy and sell books.
1   They     they    PRON    PRP    Case=Nom|Number=Plur               2   nsubj   2:nsubj|4:nsubj   _
2   buy      buy     VERB    VBP    Number=Plur|Person=3|Tense=Pres    0   root    0:root            _
3   and      and     CCONJ   CC     _                                  4   cc      4:cc              _
4   sell     sell    VERB    VBP    Number=Plur|Person=3|Tense=Pres    2   conj    0:root|2:conj     _
5   books    book    NOUN    NNS    Number=Plur                        2   obj     2:obj|4:obj       SpaceAfter=No
6   .        .       PUNCT   .      _                                  2   punct   2:punct           _

# sent_id = 2
# text = I have no clue.
1   I       I       PRON    PRP   Case=Nom|Number=Sing|Person=1     2   nsubj   _   _
2   have    have    VERB    VBP   Number=Sing|Person=1|Tense=Pres   0   root    _   _
3   no      no      DET     DT    PronType=Neg                      4   det     _   _
4   clue    clue    NOUN    NN    Number=Sing                       2   obj     _   SpaceAfter=No
5   .       .       PUNCT   .     _                                 2   punct   _   _
"""

conll_importer = CoNLLImporter(field_list=[annotation.LEMMA, annotation.UPOS, annotation.POS])
doc = conll_importer.import_document(conll_doc)

token_vocab = Vocabulary(doc.sentences, lowercase=False)
upos_vocab = Vocabulary(doc.sentences, source="UPOS", lowercase=False)

# Converting sentences to indices for both tokens and annotations
print(token_vocab.to_indices(doc.sentences))
# [[2, 5, 3, 9, 4, 0], [1, 7, 8, 6, 0]]

print(upos_vocab.to_indices(doc.sentences))
# [[3, 5, 0, 5, 2, 4], [3, 5, 1, 2, 4]]

# Retrieving tokens and annotations from indices
token_vocab.get_symbol(4)
# books

upos_vocab.get_symbol(2)
# NOUN
```


## License

This project is licensed under the GNU General Public License Version 3 - see the [LICENSE](https://github.com/dscarvalho/saf/blob/master/LICENSE) file for details.
