##########################################################################################
# Imports
##########################################################################################
import bpy
import pathlib

from blenderline.entries.base import BaseEntry


##########################################################################################
# Item entry class
##########################################################################################
class ItemEntry(BaseEntry):
    def __init__(
        self,
        filepath: str | pathlib.Path,
        label: str,
        object_name: str,
        min_margin_distance: float,
        max_lateral_distance: float,
        relative_frequency: float = 1,
    ) -> None:
        """ Registered item entry.

        Args:
            filepath (str | pathlib.Path): absolute filepath to item .blend asset.
            label (str): label category of object.
            object_name (str): name of object in item .blend file.
            min_margin_distance (float): minimum distance (in Blender units) other items
                need to be away from this item. Distance is computed between item center
                points.
            max_lateral_distance (float): maximum distance item can move from path.
            relative_frequency (float, optional): relative frequency with which to sample. 
                Defaults to 1.
        """        
        # Save object attributes
        self.filepath = filepath
        self.label = label
        self.object_name = object_name
        self.min_margin_distance = min_margin_distance
        self.max_lateral_distance = max_lateral_distance
        self.relative_frequency = relative_frequency