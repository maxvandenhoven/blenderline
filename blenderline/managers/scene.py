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
