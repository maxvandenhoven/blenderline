##########################################################################################
# Imports
##########################################################################################
import bpy

from blenderline.collections import BackgroundCollection


##########################################################################################
# Background manager class
##########################################################################################
class BackgroundManager:
    """ Manager for background-related operations, such as grabbing the background object 
        and setting a random background.
    """

    def __init__(
        self, 
        background_object_name: str, 
        background_collection: BackgroundCollection
    ) -> None:
        """ Create background manager.

        Args:
            background_object_name (str): name of background object in scene.
            background_collection (BackgroundCollection): collection of background entries.
        """        
        # Save object attributes
        self.background_object_name = background_object_name
        self.background_collection = background_collection


    def initialize(self) -> None:
        """ Get background object. """
        # Get background object by name.
        self.background_object = bpy.data.objects[self.background_object_name]


    def sample(self) -> None:
        """ Sample background entry from collection and apply it. """
        # Sample background entry from collection and apply it to background object
        background_entry = self.background_collection.sample()
        background_entry.set(self.background_object)