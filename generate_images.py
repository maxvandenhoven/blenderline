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


    item_manager = settings.get_item_manager()
    item_manager.initialize()

    for _ in range(3):
        location, normal_global_xy, normal_local_z = item_manager.path_reference.sample()
        
        item = item_manager.item_collection.sample().spawn(location)
        item.orient_to_vector(normal_local_z)


if __name__ == "__main__":
    main()