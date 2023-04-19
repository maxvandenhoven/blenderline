##########################################################################################
# Imports
##########################################################################################
import bpy


##########################################################################################
# Item reference class
##########################################################################################
class ItemReference:
    """ Reference to spawned item object in scene. """

    def __init__(
        self,
        item_object: bpy.types.Object,
        reference_entry, # No type hint to prevent circular import
    ) -> None:
        """ Create reference to item object in scene.

        Args:
            object_name (str): name of object in scene.
            reference_entry (ItemEntry): entry used to create referenced object.
        """        
        # Save object attributes
        self.item_object = item_object
        self.reference_entry = reference_entry