##########################################################################################
# Imports
##########################################################################################
import bpy

from blenderline.collections import ItemCollection
from blenderline.references import PathReference


##########################################################################################
# Item manager class
##########################################################################################
class ItemManager:
    """ Manager for item-related operations, such as spawning multiple items randomly 
        along the defined path object.    
    """

    def __init__(
        self,
        path_object_name: str,
        spawn_probability: float,
        max_tries: int,
        max_items: int,
        item_collection: ItemCollection,
    ) -> None:
        """ Create item manager.

        Args:
            path_object_name (str): name of path object in scene.
            spawn_probability (float): probability to spawn a new item.
            max_tries (int): maximum number of times to attempt to spawn an item. Spawning
                may fail due to item minimum margin distance collisions.
            max_items (int): maximum number of items to spawn.
            item_collection (ItemCollection): collection of item entries.
        """        
        # Save object attributes
        self.path_object_name = path_object_name
        self.spawn_probability = spawn_probability
        self.max_tries = max_tries
        self.max_items = max_items
        self.item_collection = item_collection

    
    def initialize(self) -> None:
        """ Get path reference object. """
        # Get path object by name and wrap it in a path reference object.
        path_object = bpy.data.objects[self.path_object_name]
        self.path_reference = PathReference(path_object)