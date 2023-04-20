##########################################################################################
# Imports
##########################################################################################
import pathlib

import bpy


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
        self._load_scene()
        self._configure_camera()
        self._configure_render_settings()


    def _load_scene(self) -> None:
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


    def _configure_camera(self) -> None:
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


    def _configure_render_settings(self) -> None:
        """ Configure render settings. """
        # Enable object pass indexin view layer.
        bpy.context.scene.view_layers[0].use_pass_object_index = True

        # Enable nodes on scene compositor and get node tree.
        bpy.context.scene.use_nodes = True
        node_tree = bpy.context.scene.node_tree
        nodes = node_tree.nodes

        # Clear all nodes.
        nodes.clear()

        # Add Render Layers node.
        render_layers_node: bpy.types.CompositorNodeRLayers = nodes.new("CompositorNodeRLayers")
        render_layers_node.location = (-300, 0)

        # Add Divice node.
        divide_node: bpy.types.CompositorNodeMath = nodes.new("CompositorNodeMath")
        divide_node.operation = "DIVIDE"
        divide_node.inputs[1].default_value = 255
        divide_node.location = (0, -300)

        # Add File Output node. Save node as instance attribute to change output path.
        self.file_output_node: bpy.types.CompositorNodeOutputFile = nodes.new("CompositorNodeOutputFile")
        self.file_output_node.file_slots.new("Segmentation")
        self.file_output_node.format.color_mode = "RGB"
        self.file_output_node.location = (300, 0)


        # Link nodes.
        links = node_tree.links
        _ = links.new(
            input=render_layers_node.outputs["Image"],
            output=self.file_output_node.inputs["Image"],
        )
        _ = links.new(
            input=render_layers_node.outputs["IndexOB"],
            output=divide_node.inputs[0],
        )
        _ = links.new(
            input=divide_node.outputs["Value"],
            output=self.file_output_node.inputs["Segmentation"],
        )


    def render(self, output_folder: pathlib.Path) -> None:
        """ Render image and segmentation mask to output folder.

        Args:
            output_folder (pathlib.Path): absolute filepath to desired output folder.
        """        
        # Set output folder on compositor nodes.
        self.file_output_node.base_path = str(output_folder)

        # Start render.
        bpy.ops.render.render()

        
