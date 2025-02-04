from distutils.core import setup

setup(
    name='saf-nlp',
    version='0.5.2',
    packages=['saf', 'saf.test', 'saf.constants', 'saf.importers', 'saf.importers.tokenizers', 'saf.annotators',
              'saf.data_model', 'saf.formatters'],
    url='',
    license='',
    author=['Danilo S. Carvalho', 'Vu Duc Tran'],
    author_email=['danilo.carvalho@manchester.ac.uk', 'vu.tran@jaist.ac.jp'],
    description='Simple Annotation Framework',
    install_requires=[
        'nltk',
        'regex'
    ]
)
