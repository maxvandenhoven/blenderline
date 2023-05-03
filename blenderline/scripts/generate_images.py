##########################################################################################
# Imports
##########################################################################################
import argparse
import pathlib
import sys

# Add base dir to PATH for module discovery within Blender
blenderline_dir = pathlib.Path(__file__).parent.parent.parent
sys.path.append(str(blenderline_dir))

from blenderline.settings import ImageDatasetSettings


##########################################################################################
# Main script
##########################################################################################
def main() -> None:
    # Build parser for arguments supplied to blender after "--"
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--config",
        metavar="<filepath>",
        help="location of config file",
        required=True,
    )
    parser.add_argument(
        "-b", "--base-dir",
        metavar="<filepath>",
        help="location from which BlenderLine is called",
        required=True,
    )

    # Parse arguments after "--".
    if "--" not in sys.argv:
        args = parser.parse_args([])
    else:
        args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:])

     # Get settings object.
    image_dataset_settings = ImageDatasetSettings(
        base_dir=pathlib.Path(args.base_dir),
        filepath=pathlib.Path(args.config),
    )

    # Generate dataset.
    image_dataset_generator = image_dataset_settings.get_dataset_generator()
    image_dataset_generator.initialize()
    image_dataset_generator.generate_dataset()


if __name__ == "__main__":
    main()