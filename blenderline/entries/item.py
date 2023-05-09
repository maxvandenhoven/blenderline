import pathlib
import secrets

import bpy

from blenderline.entries.base import BaseEntry
from blenderline.references.item import ItemReference


class ItemEntry(BaseEntry):
    """Item entry."""

    def __init__(
        self,
        filepath: pathlib.Path,
        label: int,
        object_name: str,
        min_margin_distance: float,
        max_lateral_distance: float,
        relative_frequency: float,
    ) -> None:
        """Create item entry.

        Args:
            filepath (pathlib.Path): absolute filepath to item .blend asset.
            label (int): label index of object.
            object_name (str): name of object in item .blend file.
            min_margin_distance (float): minimum distance (in Blender units) other items
                need to be away from this item. Distance is computed between item center
                points.
            max_lateral_distance (float): maximum distance item can move from path.
            relative_frequency (float): relative frequency with which to sample.
        """
        # Save object attributes
        self.filepath = filepath
        self.label = label
        self.object_name = object_name
        self.min_margin_distance = min_margin_distance
        self.max_lateral_distance = max_lateral_distance
        self.relative_frequency = relative_frequency

    def spawn(self, location: tuple[float, float, float]) -> ItemReference:
        """Instantiate item object in the scene at a given location.

        Args:
            location (tuple[float, float, float]): location to spawn object at.

        Returns:
            ItemReference: reference to spawned item object.
        """
        scene_item_collection = bpy.data.collections["items"]

        with bpy.data.libraries.load(str(self.filepath)) as (data_from, data_to):
            data_to.objects = [
                name for name in data_from.objects if name == self.object_name
            ]

        for object in data_to.objects:
            if object is not None:
                scene_item_collection.objects.link(object)

        # Generate random name for object in scene to prevent object name
        # collisions when multiple objects are added to the scene
        scene_object_name = str(self.label) + "__" + secrets.token_hex(8)

        # Select spawned object and set proper name and location
        item_object = bpy.data.objects[self.object_name]
        item_object.name = scene_object_name
        item_object.location = location

        return ItemReference(item_object, self)
