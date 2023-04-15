##########################################################################################
# Imports
##########################################################################################
from abc import ABC, abstractmethod


##########################################################################################
# Base entry class
##########################################################################################
class BaseEntry(ABC):
    """ Base class for entries that are stored in a collection. """

    @property
    @abstractmethod
    def relative_frequency(self) -> float:
        """ Relative frequency of the entry. """
        