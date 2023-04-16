##########################################################################################
# Imports
##########################################################################################
import sys
import pathlib

# Add base dir to PATH for module discovery within Blender
base_dir = pathlib.Path(__file__).parent
sys.path.append(str(base_dir))

from blenderline.settings import ImageGenerationSettings


##########################################################################################
# Main script
##########################################################################################
def main() -> None:
    settings = ImageGenerationSettings(base_dir, "config/example_beer/image.json")

    # Initialize scene by loading scene assets and configuring camera
    scene_manager = settings.get_scene_manager()
    scene_manager.initialize()


if __name__ == "__main__":
    main()