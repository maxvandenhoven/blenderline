from abc import ABC


class BaseEntry(ABC):
    """Base class for entries that are stored in a collection."""

    relative_frequency: float
