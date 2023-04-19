##########################################################################################
# Imports
##########################################################################################
import bpy


##########################################################################################
# Path reference class
##########################################################################################
class PathReference:
    """ Reference to path object in scene. """

    def __init__(self, path_object: bpy.types.Object) -> None:
        """ Create reference to path object in scene.

        Args:
            path_object (bpy.types.Object): path object in scene.
        """        
        # Save object attributes
        self.path_object = path_object