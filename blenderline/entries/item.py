##########################################################################################
# Imports
##########################################################################################
import bpy
import pathlib
import secrets

from blenderline.entries.base import BaseEntry
from blenderline.references.item import ItemReference


##########################################################################################
# Item entry class
##########################################################################################
class ItemEntry(BaseEntry):
    """ Item entry. """

    def __init__(
        self,
        filepath: str | pathlib.Path,
        label: str,
        object_name: str,
        min_margin_distance: float,
        max_lateral_distance: float,
        relative_frequency: float = 1,
    ) -> None:
        """ Create item entry.

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


    def spawn(self, location: tuple[float, float, float]) -> ItemReference:
        """ Instantiate item object in the scene at a given location.

        Args:
            location (tuple[float, float, float]): location to spawn object at.

        Returns:
            ItemReference: reference to spawned item object.
        """                
        # Deselect everything in the scene to be safe.
        bpy.ops.object.select_all(action='DESELECT')

        # Add object to scene (added object will have name `self.object_name`)
        bpy.ops.wm.append(
            filepath=str(self.filepath),
            directory=str(self.filepath / "Object"),
            filename=self.object_name
        )

        # Generate random name for object in scene to prevent object name 
        # collisions when multiple objects are added to the scene
        scene_object_name = self.label + "__" + secrets.token_urlsafe(10)
        
        # Select spawned object and set proper name and location
        obj = bpy.data.objects[self.object_name]
        obj.name = scene_object_name
        obj.location = location

        return ItemReference(scene_object_name, self)
