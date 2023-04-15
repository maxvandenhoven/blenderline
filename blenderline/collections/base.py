##########################################################################################
# Imports
##########################################################################################
import random

from typing import TypeVar, Generic

from blenderline.entries.base import BaseEntry


##########################################################################################
# Custom types
##########################################################################################
EntryType = TypeVar("EntryType", bound=BaseEntry)


##########################################################################################
# Base collection class
##########################################################################################
class BaseCollection(Generic[EntryType]):
    """ Base class for collections. """

    def __init__(self) -> None:
        """ Initialize empty collection. """
        self.entries: list[EntryType] = []

    
    def register(self, entry: EntryType) -> None:
        """ Register new entry to collection.

        Args:
            entry (EntryType): entry to register to the collection.
        """        
        self.entries.append(entry)


    @property
    def total_frequency(self) -> float:
        """ Total frequency of all entries in the collection.

        Returns:
            float: total frequency.
        """        
        return sum(entry.relative_frequency for entry in self.entries)


    def sample(self) -> EntryType:
        """ Sample from registered entries according to computed probabilities.

        Returns:
            EntryType: sampled entry.
        """        
        # Compute individual entry sampling probabilities and sample accordingly.
        weights = [entry.relative_frequency/self.total_frequency for entry in self.entries]
        return random.choices(self.entries, weights=weights, k=1)[0]