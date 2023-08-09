import argparse
import pathlib
import sys

blenderline_dir = pathlib.Path(__file__).parent.parent
sys.path.append(str(blenderline_dir))

from blenderline.scripts.python import run_convert, run_generate  # noqa: E402


def cli_parser() -> argparse.ArgumentParser:
    # Main parser
    parser = argparse.ArgumentParser(
        prog="blenderline",
        description="BlenderLine: a pipeline for generating synthetic production line images.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(
        dest="command", help="Select a BlenderLine command to run:"
    )

    # Generate subparser
    generate_parser = subparsers.add_parser(
        name="generate",
        help="Generate a BlenderLine dataset from a configuration file.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    generate_required_parser = generate_parser.add_argument_group("required arguments")
    generate_required_parser.add_argument(
        "--config",
        required=True,
        metavar="<filepath>",
        help="Absolute or relative location of the configuration file.",
    )
    generate_optional_parser = generate_parser.add_argument_group("optional arguments")
    generate_optional_parser.add_argument(
        "--target",
        required=False,
        metavar="<filepath>",
        help="Absolute or relative location of the generated dataset.\n"
        "By default, BlenderLine generates the dataset in the current working directory.",
    )
    generate_optional_parser.add_argument(
        "--blender",
        required=False,
        metavar="<filepath>",
        help="Absolute location of the folder in which Blender is installed.\n"
        "By default, BlenderLine assumes that Blender is added to the system path.",
    )

    # Convert subparser
    convert_parser = subparsers.add_parser(
        name="convert",
        help="Convert a BlenderLine dataset to another format, e.g., yolo.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    convert_required_parser = convert_parser.add_argument_group("required arguments")
    format_choices = ["yolo_detection"]
    convert_required_parser.add_argument(
        "--format",
        required=True,
        choices=format_choices,
        metavar="<option>",
        help=f"Type of dataset to convert to. Must be in {{{', '.join(format_choices)}}}",
    )
    convert_required_parser.add_argument(
        "--source",
        required=True,
        metavar="<filepath>",
        help="Absolute or relative location of the BlenderLine dataset to convert.",
    )
    convert_optional_parser = convert_parser.add_argument_group("optional arguments")
    convert_optional_parser.add_argument(
        "--target",
        required=True,
        metavar="<filepath>",
        help="Absolute or relative location of the converted dataset.",
    )
    convert_optional_parser.add_argument(
        "--minarea",
        required=False,
        default=0.005,
        metavar="<float>",
        help="Minimum area an object mask must have to be included in the dataset.\n"
        "Area is defined as (num_pixels_object_mask/num_pixels_total_image).\n"
        "By default, BlenderLine omits masks with an area less than 0.005.",
    )
    convert_flags_parser = convert_parser.add_argument_group("flags")
    convert_flags_parser.add_argument(
        "--remove",
        required=False,
        action="store_true",
        help="If set, the source dataset is removed after conversion. While technically\n"
        "possible, it is discouraged to add the converted dataset to the source dataset\n"
        "by setting neither --target nor --remove.",
    )

    return parser


def cli():
    parser = cli_parser()

    args = parser.parse_args()

    if args.command == "generate":
        run_generate(config=args.config, target=args.target, blender=args.blender)
    elif args.command == "convert":
        run_convert(
            format=args.format,
            source=args.source,
            target=args.target,
            minarea=args.minarea,
            remove=args.remove,
        )


if __name__ == "__main__":
    cli()
