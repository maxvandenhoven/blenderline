import pathlib

import bpy

from blenderline.entries.base import BaseEntry


class BackgroundEntry(BaseEntry):
    """Background entry."""

    def __init__(self, filepath: pathlib.Path, relative_frequency: float) -> None:
        """Create background entry.

        Args:
            filepath (pathlib.Path): absolute filepath to image asset.
            relative_frequency (float): relative frequency with which to sample.
        """
        # Save object attributes.
        self.filepath = filepath
        self.relative_frequency = relative_frequency

    def set(self, background_object: bpy.types.Object) -> None:
        """Apply background image to background object.

        Args:
            background_object (bpy.types.Object): object to apply background to.
        """
        # Get active material node tree.
        node_tree = background_object.active_material.node_tree
        nodes = node_tree.nodes

        # Clear all nodes.
        nodes.clear()

        # Add Texture Image node.
        node: bpy.types.ShaderNodeTexImage = nodes.new("ShaderNodeTexImage")
        texture_node = node
        texture_node.image = bpy.data.images.load(str(self.filepath))
        texture_node.location = (-300, 0)

        # Add Principled BSDF node.
        node: bpy.types.ShaderNodeBsdfPrincipled = nodes.new("ShaderNodeBsdfPrincipled")
        bsdf_node = node
        bsdf_node.location = (0, 0)

        # Add Material Output node.
        node: bpy.types.ShaderNodeOutputMaterial = nodes.new("ShaderNodeOutputMaterial")
        output_node = node
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
