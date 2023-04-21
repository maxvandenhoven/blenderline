##########################################################################################
# Imports
##########################################################################################
import pathlib

import bpy

from blenderline.entries.base import BaseEntry


##########################################################################################
# HDR entry class
##########################################################################################
class HDREntry(BaseEntry):
    """ HDR entry. """

    def __init__(
        self,
        filepath: pathlib.Path,
        relative_frequency: float,
    ) -> None:
        """ Create HDR background entry.

        Args:
            filepath (pathlib.Path): absolute filepath to HDR asset.
            relative_frequency (float): relative frequency with which to sample.
        """           
        # Save object attributes.
        self.filepath = filepath
        self.relative_frequency = relative_frequency


    def set(self, world: bpy.types.World) -> None:
        """ Set HDR as environment background.

        Args:
            world (bpy.types.World): world object to apply background to.
        
        Sources:
            - https://blender.stackexchange.com/a/209633
        """        
        # Get environment node tree of world.
        node_tree = world.node_tree
        nodes = node_tree.nodes

        # Clear all nodes.
        nodes.clear()
        
        # Add Environment Texture node.
        node: bpy.types.ShaderNodeTexEnvironment = nodes.new("ShaderNodeTexEnvironment")
        environment_node = node
        environment_node.image = bpy.data.images.load(str(self.filepath))
        environment_node.location = (-300, 0)

        # Add Background node.
        node: bpy.types.ShaderNodeBackground = nodes.new("ShaderNodeBackground")
        background_node = node
        background_node.location = (0, 0)

        # Add Output node.
        output_node = nodes.new("ShaderNodeOutputWorld")
        output_node.location = (300, 0)

        # Link nodes.
        links = node_tree.links
        _ = links.new(
            input=environment_node.outputs["Color"],
            output=background_node.inputs["Color"],
        )
        _ = links.new(
            input=background_node.outputs["Background"],
            output=output_node.inputs["Surface"],
        )