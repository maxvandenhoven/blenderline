import argparse
import pathlib
import sys

# Add base dir to PATH for module discovery within Blender
blenderline_dir = pathlib.Path(__file__).parent.parent.parent.parent
sys.path.append(str(blenderline_dir))

from blenderline.settings import ImageDatasetSettings  # noqa: E402


def main() -> None:
    # Build parser for arguments supplied to blender after "--"
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        required=True,
        metavar="<filepath>",
        help="Absolute location of the configuration file.",
    )
    parser.add_argument(
        "--target",
        required=True,
        metavar="<filepath>",
        help="Absolute location of the directory where the dataset is generated.",
    )

    # Parse arguments after "--".
    if "--" not in sys.argv:
        args = parser.parse_args([])
    else:
        args = parser.parse_args(sys.argv[sys.argv.index("--") + 1 :])

    # Get settings object.
    image_dataset_settings = ImageDatasetSettings(
        config=pathlib.Path(args.config),
        target=pathlib.Path(args.target),
    )

    # Generate dataset.
    image_dataset_generator = image_dataset_settings.get_dataset_generator()
    image_dataset_generator.initialize()
    image_dataset_generator.generate_dataset()


if __name__ == "__main__":
    main()
