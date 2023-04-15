##########################################################################################
# Item reference class
##########################################################################################
class ItemReference:
    """ Reference to spawned item object in scene. """

    def __init__(
        self,
        object_name: str,
        reference_entry, # No type hint to prevent circular import
    ) -> None:
        """ Create reference to item object in scene.

        Args:
            object_name (str): name of object in scene.
            reference_entry (ItemEntry): entry used to create referenced object.
        """        
        # Save object attributes
        self.object_name = object_name
        self.reference_entry = reference_entry