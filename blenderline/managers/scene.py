##########################################################################################
# Imports
##########################################################################################
import pathlib
import secrets

import bpy

from blenderline.references import ItemReference


##########################################################################################
# Scene manager class
##########################################################################################
class SceneManager:
    """ Manager for scene-related operations, such as loading a scene and configuring the
        camera. 
    """

    def __init__(
        self,
        filepath: pathlib.Path,
        camera_object_name: str,
        render_samples: int,
        render_use_cuda: bool,
        render_denoising: bool,
        render_resolution: list[int, int],
    ) -> None:
        """ Create scene manager.

        Args:
            filepath (pathlib.Path): absolute filepath to scene .blend asset.
            camera_object_name (str): name of camera object in scene.
            render_samples (int): number of samples to render with.
            render_use_cuda (bool): whether to use CPU (False) or CUDA GPU (True).
            render_denoising (bool): enable denoising on rendered image.
            render_resolution (list[int, int]): image resolution ([x, y]) to render at.
        """              
        # Save object attributes
        self.filepath = filepath
        self.camera_object_name = camera_object_name
        self.render_samples = render_samples
        self.render_use_cuda = render_use_cuda
        self.render_denoising = render_denoising
        self.render_resolution = render_resolution


    def initialize(self) -> None:
        """ Initialize scene using specified parameters by loading scene and configuring 
            the camera. 
        """
        self.load_scene()
        self.configure_camera()


    def load_scene(self) -> None:
        """ Load scene .blend file as main Blender file. """ 
        # Start with empty Blender file.
        bpy.ops.wm.read_factory_settings(use_empty=True)

        # Add collection to copy all scene objects to from scene .blend file.
        scene_collection = bpy.data.collections.new("scene")
        bpy.context.scene.collection.children.link(scene_collection)
        
        # Copy all objects from specified scene .blend file. Note that collection
        # organization of original scene .blend file is lost, as all objects are placed
        # in a new collection named "scene". 
        with bpy.data.libraries.load(str(self.filepath)) as (data_from, data_to):
            data_to.objects = data_from.objects

        for object in data_to.objects:
            if object is not None:
                scene_collection.objects.link(object)


    def configure_camera(self) -> None:
        """ Configure active camera in scene. """
        # Get camera object and set it as active in the scene.
        camera_object = bpy.data.objects[self.camera_object_name]
        bpy.context.scene.camera = camera_object

        # Set render engine to cycles, as eevee does not support headless rendering.
        bpy.context.scene.render.engine = "CYCLES"

        # Enable CUDA GPU
        if self.render_use_cuda:
            cycles_preferences = bpy.context.preferences.addons["cycles"].preferences
            cycles_preferences.compute_device_type = "CUDA"
            cycles_preferences.get_devices()
            bpy.context.scene.cycles.device = "GPU"

        # Configure render samples, denoising, and resolution.
        bpy.context.scene.cycles.samples = self.render_samples
        bpy.context.scene.cycles.use_denoising = self.render_denoising
        bpy.context.scene.render.resolution_x = self.render_resolution[0]
        bpy.context.scene.render.resolution_y = self.render_resolution[1]


    def reset_compositor_nodes(self) -> None:
        """ Configure render settings. """
        # Enable object pass indexin view layer.
        bpy.context.scene.view_layers[0].use_pass_object_index = True

        # Enable nodes on scene compositor and get node tree.
        bpy.context.scene.use_nodes = True
        self.node_tree = bpy.context.scene.node_tree
        self.nodes = self.node_tree.nodes

        # Clear all nodes.
        self.nodes.clear()

        # Add Render Layers node.
        node: bpy.types.CompositorNodeRLayers = self.nodes.new("CompositorNodeRLayers")
        self.render_layers_node = node
        self.render_layers_node.location = (-300, 0)

        # Generate random indentifier for image
        image_filename = "image/" + "image__" + secrets.token_hex(8) + "__"

        # Add File Output node. Save node as instance attribute to change output path.
        node: bpy.types.CompositorNodeOutputFile = self.nodes.new("CompositorNodeOutputFile")
        self.file_output_node = node
        self.file_output_node.file_slots.remove(node.inputs["Image"])
        self.file_output_node.file_slots.new(image_filename)
        self.file_output_node.format.color_mode = "RGB"
        self.file_output_node.location = (300, 0)

        # Link nodes.
        self.links = self.node_tree.links
        _ = self.links.new(
            input=self.render_layers_node.outputs["Image"],
            output=self.file_output_node.inputs[image_filename],
        )


    def add_item_reference_render_output(self, item_reference: ItemReference) -> None:
        """ Add nodes to get segmentation mask corresponding to an item reference.

        Args:
            item_reference (ItemReference): item reference to generate mask output for.
        """        
        # Generate object segmentation mask output filename
        mask_filename = "masks/" + item_reference.item_object.name + "__"

        # Add output file for object segmentation mask to File Output node.
        self.file_output_node.file_slots.new(mask_filename)

        # Add ID Mask node.
        node: bpy.types.CompositorNodeIDMask = self.nodes.new("CompositorNodeIDMask")
        id_mask_node = node
        id_mask_node.index = item_reference.pass_index
        id_mask_node.use_antialiasing = True

        # Link nodes.
        _ = self.links.new(
            input=self.render_layers_node.outputs["IndexOB"],
            output=id_mask_node.inputs["ID value"],
        )
        _ = self.links.new(
            input=id_mask_node.outputs["Alpha"],
            output=self.file_output_node.inputs[mask_filename],
        )


    def render(
        self, 
        output_folder: pathlib.Path, 
        item_references: list[ItemReference],
    ) -> None:
        """ Render current scene, outputting rendered image and all item segmentation 
            masks. Rendered image will have filename "image__0001.png". Segmentation masks
            will have filename "<label ID>__<random item ID>__0001.png".

        Args:
            output_folder (pathlib.Path): folder to store images in.
            item_references (list[ItemReference]): list of item refereces to generate 
                masks for.
        """        
        # Reset compositor nodes.
        self.reset_compositor_nodes()

        # Set output folder.
        self.file_output_node.base_path = str(output_folder)

        # Add item references to segmentation mask outputs.
        for item_reference in item_references:
            self.add_item_reference_render_output(item_reference)

        # Start render.
        bpy.ops.render.render()

        
