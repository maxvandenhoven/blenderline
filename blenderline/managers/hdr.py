##########################################################################################
# Imports
##########################################################################################
import bpy

from blenderline.collections import HDRCollection


##########################################################################################
# HDR manager class
##########################################################################################
class HDRManager:
    """ Manager for HDR-related operations, such as creating a world texture and sampling
        and setting a random HDR background. 
    """

    def __init__(self, hdr_collection: HDRCollection) -> None:
        """ Create HDR background manager.

        Args:
            hdr_collection (HDRCollection): collection of HDR background entries.
        """        
        # Save object attributes.
        self.hdr_collection = hdr_collection

    
    def initialize(self) -> None:
        """ Create world texture with nodes to put HDR background texture on. """
        # Create new world texture and enable nodes.
        self.world = bpy.data.worlds.new("world")
        self.world.use_nodes = True

        # Set new world as active world in scene.
        bpy.context.scene.world = self.world


    def sample(self) -> None:
        """ Sample HDR background entry from collection and apply it. """
        # Sample HDR entry from collection and apply it to initialized world texture.
        hdr_entry = self.hdr_collection.sample()
        hdr_entry.set(self.world)





