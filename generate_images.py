##########################################################################################
# Imports
##########################################################################################
import pathlib
import sys

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


    hdr_manager = settings.get_hdr_manager()
    hdr_manager.initialize()
    hdr_manager.sample()

    background_manager = settings.get_background_manager()
    background_manager.initialize()
    background_manager.sample()


    item_collection = settings.get_item_collection()

    item_1 = item_collection.sample().spawn((0, 0, 0))
    item_2 = item_collection.sample().spawn((0.24, 0, 0))
    item_3 = item_collection.sample().spawn((-0.24, 0, 0))


if __name__ == "__main__":
    main()