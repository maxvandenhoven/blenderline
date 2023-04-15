##########################################################################################
# Imports
##########################################################################################
import random

from abc import ABC, abstractmethod
from typing import TypeVar, Generic


##########################################################################################
# Base registered object class
##########################################################################################
class RegisteredBase(ABC):
    @property
    @abstractmethod
    def relative_frequency(self) -> float:
        """ Relative frequency of the object. """


##########################################################################################
# Base collection class
##########################################################################################
RegisteredType = TypeVar("RegisteredType", bound=RegisteredBase)

class CollectionBase(Generic[RegisteredType]):
    def __init__(self) -> None:
        """ Initialize empty collection. """
        self.registered: list[RegisteredType] = []

    
    def register(self, obj: RegisteredType) -> None:
        """ Register new object to collection.

        Args:
            obj (RegisteredType): object to register to collection.
        """        
        self.registered.append(obj)


    @property
    def total_frequency(self) -> float:
        """ Total frequency of all items in the collection.

        Returns:
            float: total frequency.
        """        
        return sum(obj.relative_frequency for obj in self.registered)


    def sample(self) -> RegisteredType:
        """ Sample from registered objects according to computed probabilities.

        Returns:
            RegisteredType: sampled registered object.
        """        
        # Compute individual object sampling probabilities and sample accordingly.
        weights = [obj.relative_frequency/self.total_frequency for obj in self.registered]
        return random.choices(self.registered, weights=weights, k=1)[0]