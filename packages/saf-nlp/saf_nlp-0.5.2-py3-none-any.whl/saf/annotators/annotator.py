__author__ = "Danilo S. Carvalho <danilo@jaist.ac.jp>"

from abc import ABC
from abc import abstractmethod
from typing import Iterable
from saf import Annotable


class Annotator(ABC):
    def __init__(self):
        """Annotator constructor

        Constructs an annotator object that includes or modify annotations for objects in the data model.

        :return: new Annotator instance.
        """
        pass


    @abstractmethod
    def annotate(self, items: Iterable[Annotable]):
        """Annotates all items in the input iterable in place

        Args:
            items (Iterable[Annotable]): Collection of objects to be annotated.

        """

        raise NotImplementedError()


class AnnotationError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
