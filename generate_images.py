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
    # Get settings object.
    image_dataset_settings = ImageDatasetSettings(
        base_dir=base_dir, 
        filepath="config/example_beer/image.json"
    )

    # Generate dataset.
    image_dataset_generator = image_dataset_settings.get_dataset_generator()
    image_dataset_generator.initialize()
    image_dataset_generator.generate_dataset()


if __name__ == "__main__":
    main()