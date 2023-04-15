##########################################################################################
# Imports
##########################################################################################
import bpy
import pathlib

from blenderline.entries.base import BaseEntry


##########################################################################################
# Background registered object class
##########################################################################################
class BackgroundEntry(BaseEntry):
    def __init__(
        self,
        filepath: str | pathlib.Path,
        relative_frequency: float = 1,
    ) -> None:
        """ Registered background entry.

        Args:
            filepath (str | pathlib.Path): absolute filepath to image asset.
            relative_frequency (float, optional): relative frequency with which to sample. 
                Defaults to 1.
        """           
        # Save object attributes.
        self.filepath = filepath
        self.relative_frequency = relative_frequency


    def set(self, background_object_name: str) -> None:
        """ Apply background image to background object.

        Args:
            background_object_name (str): name of object to apply background to.
        """               
        # Get background object.
        background_obj = bpy.data.objects[background_object_name]

        # Get active material node tree.
        node_tree = background_obj.active_material.node_tree
        nodes = node_tree.nodes

        # Clear all nodes.
        nodes.clear()

        # Add Texture Image node.
        texture_node = nodes.new("ShaderNodeTexImage")
        texture_node.image = bpy.data.images.load(str(self.filepath))
        texture_node.location = (-300, 0)

        # Add Principled BSDF node.
        bsdf_node = nodes.new("ShaderNodeBsdfPrincipled")
        bsdf_node.location = (0, 0)

        # Add Material Output node.
        output_node = nodes.new("ShaderNodeOutputMaterial")
        output_node.location = (300, 0)

        # Link nodes.
        links = node_tree.links
        _ = links.new(
            input=texture_node.outputs["Color"],
            output=bsdf_node.inputs["Base Color"],
        )
        _ = links.new(
            input=texture_node.outputs["Alpha"],
            output=bsdf_node.inputs["Alpha"],
        )
        _ = links.new(
            input=bsdf_node.outputs["BSDF"],
            output=output_node.inputs["Surface"],
        )