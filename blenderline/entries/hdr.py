##########################################################################################
# Imports
##########################################################################################
import bpy
import pathlib

from blenderline.entries.base import BaseEntry


##########################################################################################
# HDR entry class
##########################################################################################
class HDREntry(BaseEntry):
    def __init__(
        self,
        filepath: str | pathlib.Path,
        relative_frequency: float = 1,
    ) -> None:
        """ Registered HDR background entry.

        Args:
            filepath (str | pathlib.Path): absolute filepath to HDR asset.
            relative_frequency (float, optional): relative frequency with which to sample. 
                Defaults to 1.
        """           
        # Save object attributes.
        self.filepath = filepath
        self.relative_frequency = relative_frequency


    def set(self) -> None:
        """ Set HDR as environment background.
        
        Sources:
            - https://blender.stackexchange.com/a/209633
        """        
        # Get environment node tree of current scene.
        node_tree = bpy.context.scene.world.node_tree
        nodes = node_tree.nodes

        # Clear all nodes.
        nodes.clear()
        
        # Add Environment Texture node.
        environment_node = nodes.new("ShaderNodeTexEnvironment")
        environment_node.image = bpy.data.images.load(str(self.filepath))
        environment_node.location = (-300, 0)

        # Add Background node.
        background_node = nodes.new("ShaderNodeBackground")
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