##########################################################################################
# Imports
##########################################################################################
import bpy
import mathutils


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
            object_name (str): item object in scene.
            reference_entry (ItemEntry): entry used to create referenced object.
        """        
        # Save object attributes.
        self.item_object = item_object
        self.reference_entry = reference_entry

        # Prepare object for rotation by saving current orientation (up on initialization)
        self.orientation = mathutils.Vector((0, 0, 1))
        self.item_object.rotation_mode = 'QUATERNION'


    def orient_to_vector(self, desired_orientation: mathutils.Vector) -> None:
        """ Rotate object so that orientation (object local z axis) aligns with desired
            direction.

        Args:
            desired_orientation (mathutils.Vector): desired local z orientation of object.
        """        
        # Determine normalized rotation quaternion between current and desired orientation.
        rotation_quaternion = self.orientation.rotation_difference(desired_orientation)
        rotation_quaternion.normalize()

        # Apply rotation and update object orientation.
        self.item_object.rotation_quaternion = rotation_quaternion
        self.orientation = desired_orientation
