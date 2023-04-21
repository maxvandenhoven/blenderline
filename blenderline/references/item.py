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
        self.item_object.rotation_mode = "QUATERNION"

        # Set default pass index of object
        self.pass_index = 0


    def set_pass_index(self, pass_index: int) -> None:
        """ Set pass index of object. 

        Args:
            pass_index (int): pass index to set on object. Must be between 0 and 255.
        """        
        self.item_object.pass_index = pass_index
        self.pass_index = pass_index


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


    def location_is_valid(
        self, 
        proposed_location: mathutils.Vector, 
        proposed_min_margin_distance: float,
    ) -> bool:
        """ Check if a proposed location is far enough away from object, i.e., distance 
            between the current object location and the proposed location is above the 
            specified minimum margin distance defined on the reference item entry.

        Args:
            proposed_location (mathutils.Vector): proposed location for new item.
            proposed_min_margin_distance (float): minimum margin distance for proposed item.

        Returns:
            bool: True if proposed location is valid w.r.t. this item.
        """        
        # Get location and minimum margin distance of spawned object
        current_location: mathutils.Vector = self.item_object.location
        current_min_margin_distance = self.reference_entry.min_margin_distance

        # Compute distance between current spawned object and proposed location
        distance = (current_location - proposed_location).length

        # Check if distance satisfies both minimum margin distances
        return distance > max(current_min_margin_distance, proposed_min_margin_distance) 
