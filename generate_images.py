##########################################################################################
# Imports
##########################################################################################
import pathlib
import sys

# Add base dir to PATH for module discovery within Blender
base_dir = pathlib.Path(__file__).parent
sys.path.append(str(base_dir))

from blenderline.settings import ImageDatasetSettings


##########################################################################################
# Main script
##########################################################################################
def main() -> None:
    settings = ImageDatasetSettings(base_dir, "config/example_beer/image.json")

    # Get all managers.
    scene_manager = settings.get_scene_manager()
    hdr_manager = settings.get_hdr_manager()
    background_manager = settings.get_background_manager()
    item_manager = settings.get_item_manager()

    # Initialize all managers.
    scene_manager.initialize()
    hdr_manager.initialize()
    background_manager.initialize()
    item_manager.initialize()

    # Run image generation steps once.
    hdr_manager.sample()
    background_manager.sample()
    item_manager.sample()
    item_manager.assign_pass_indices()
    scene_manager.render(
        output_folder=pathlib.Path.home() / "Desktop/train/0",
        item_references=item_manager.item_references
    )
    item_manager.clear()


if __name__ == "__main__":
    main()