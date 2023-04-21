##########################################################################################
# Imports
##########################################################################################
import math
import random

import bpy
import mathutils

from blenderline.collections import ItemCollection
from blenderline.references import ItemReference, PathReference


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
        self.item_references: list[ItemReference] = []

    
    def initialize(self) -> None:
        """ Get path reference object. """
        # Get path object by name and wrap it in a path reference object.
        path_object = bpy.data.objects[self.path_object_name]
        self.path_reference = PathReference(path_object)

        # Create collection in which spawned items are placed for easy tracking
        self.scene_item_collection = bpy.data.collections.new("items")
        bpy.context.scene.collection.children.link(self.scene_item_collection)


    def location_is_valid(
        self, 
        proposed_location: mathutils.Vector, 
        proposed_min_margin_distance: float,
    ) -> bool:
        """ Check if proposed object location is valid with respect to all currently 
            spawned items.

        Args:
            proposed_location (mathutils.Vector): proposed location for new item.
            proposed_min_margin_distance (float): minimum margin distance for proposed item.

        Returns:
            bool: True if proposed location is valid w.r.t. all spawned items.
        """        
        # Return False if any spawned object returns not valid.
        for item_reference in self.item_references:
            if not item_reference.location_is_valid(
                proposed_location, 
                proposed_min_margin_distance
            ):
                return False
            
        return True
    

    def max_items_reached(self) -> bool:
        """ Checks if another item may be spawned according to maximum number of items
            configured.  
        """
        num_spawned_items = len(self.item_references)
        return num_spawned_items >= self.max_items
    

    def trial_success(self) -> bool:
        """ Perform random draw according to success probability based on number of items
            currently spawned. """
        num_spawned_items = len(self.item_references)
        success_probability = math.exp((self.spawn_probability -1)*num_spawned_items)
        return random.random() < success_probability

    

    def sample(self) -> None:
        """ Sample a set of items along the path. Items are sampled until either the
            maximum number of items is reached, the random trial fails, or an item cannot
            be spawned within a maximum number of tries. 
        """        
        # Keep track of amount of tries to 
        tries = 0

        # Keep sampling until maximum items have been reached or random trial fails.
        while not self.max_items_reached() and self.trial_success() and tries < self.max_tries:
            # Sample item entry from the collection to spawn in.
            item_entry = self.item_collection.sample()

            # Sample location along the path and compute normals.
            location, normal_lateral, normal_upright = self.path_reference.sample()

            # Randomly offset item laterally by sampling random number in [-1, 1] and
            # multiplying by the item's maximum lateral offset. Multiplying this offset
            # distance with the lateral normal vector determines the change to the 
            # initially sampled location.
            offset_fraction = random.random() * 2 - 1
            offset_distance = offset_fraction * item_entry.max_lateral_distance
            lateral_offset_vector = normal_lateral * offset_distance
            location += lateral_offset_vector

            # Check validity of sampled location and place item if valid.
            if self.location_is_valid(location, item_entry.max_lateral_distance):
                # Spawn item and save reference.
                item_reference = item_entry.spawn(location)
                self.item_references.append(item_reference)

                # Orient item to path upright normal.
                item_reference.orient_to_vector(normal_upright)
                
                # Set tries to 0 if an item could be spawned succesfully.
                tries = 0
            else:
                # Increment counter if sampled location is not valid.
                tries += 1

    
    def assign_pass_indices(self) -> None:
        """ Assign pass indices to all currently spawned items. """
        # Set pass index on every spawned item.
        for pass_index, item_reference in enumerate(self.item_references):
            item_reference.set_pass_index(pass_index + 1) # Add one as background is 0.
