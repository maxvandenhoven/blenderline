##########################################################################################
# Imports
##########################################################################################
import bpy
import pathlib


##########################################################################################
# Scene manager class
##########################################################################################
class SceneManager:
    """ Manager for scene-related operations, such as loading a scene and configuring the
        camera. 
    """

    def __init__(
        self,
        filepath: str,
        camera_object_name: str,
        render_samples: int,
        render_denoising: bool,
        render_resolution: list[int, int],
    ) -> None:
        """ Create scene manager.

        Args:
            filepath (str): absolute filepath to scene .blend asset.
            camera_object_name (str): name of camera object in scene.
            render_samples (int): number of samples to render with.
            render_denoising (bool): enable denoising on rendered image.
            render_resolution (list[int, int]): image resolution ([x, y]) to render at.
        """              
        # Save object attributes
        self.filepath = filepath
        self.camera_object_name = camera_object_name
        self.render_samples = render_samples
        self.render_denoising = render_denoising
        self.render_resolution = render_resolution


    def _load_scene(self) -> None:
        """ Load scene .blend file as main Blender file. """          
        bpy.ops.wm.open_mainfile(filepath=self.filepath)


    def _configure_camera(self) -> None:
        """ Configure active camera in scene. """
        # Get camera object and set it as active in the scene.
        camera_object = bpy.data.objects[self.camera_object_name]
        bpy.context.scene.camera = camera_object

        # Configure render samples, denoising, and resolution.
        bpy.context.scene.cycles.samples = self.render_samples
        bpy.context.scene.cycles.use_denoising = self.render_denoising
        bpy.context.scene.render.resolution_x = self.render_resolution[0]
        bpy.context.scene.render.resolution_y = self.render_resolution[1]


    def initialize(self) -> None:
        """ Initialize scene using specified parameters by loading scene and configuring 
            the camera. 
        """
        self._load_scene()
        self._configure_camera()


