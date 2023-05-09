import argparse
import os
import pathlib
import signal
import subprocess
import sys

base_dir = pathlib.Path(__file__).parent.parent
sys.path.append(str(base_dir))


def cli():
    # Main parser object.
    parser = argparse.ArgumentParser(
        prog="blenderline",
        description="BlenderLine: a pipeline for generating synthetic production line images",
    )

    # Required arguments: generation mode and config file.
    required_parser = parser.add_argument_group("required named arguments")
    required_parser.add_argument(
        "-m",
        "--mode",
        metavar="<option>",
        choices=["images", "video"],
        help="type of data to generate. Allowed values are images and video",
        required=True,
    )
    required_parser.add_argument(
        "-c",
        "--config",
        metavar="<filepath>",
        help="location of config file",
        required=True,
    )

    # Optional arguments: Blender installation path.
    optional_parser = parser.add_argument_group("optional named arguments")
    optional_parser.add_argument(
        "-b",
        "--blender-path",
        metavar="<filepath>",
        help="location of folder containg blender executable. Use quotes if filepath contains spaces",
    )

    # Parse arguments.
    args = parser.parse_args()

    # Convert given config filepath to absolute path.
    config_filepath = str(pathlib.Path(os.path.abspath(args.config)))

    # Convert given Blender filepath to absolute path.
    if args.blender_path:
        blender_path = pathlib.Path(os.path.abspath(args.blender_path))
        blender_run_path = str(blender_path / "blender")
    else:
        blender_run_path = "blender"

    # Get script to execute in Blender context from selected generation mode.
    if args.mode == "images":
        script_path = str(base_dir / "blenderline" / "scripts" / "generate_images.py")
    else:
        raise NotImplementedError("Video generation is not yet implemented.")

    # Start Blender process.
    p = subprocess.Popen(
        [
            blender_run_path,
            "-b",
            "--python",
            script_path,
            "--",
            "--config",
            config_filepath,
            "--base-dir",
            os.getcwd(),
        ]
    )

    def cleanup():
        """Handle cleanup of temporary resources."""
        print("placeholder")

    def handle_sigterm(_signum, _frame):
        cleanup()
        p.terminate()

    signal.signal(signal.SIGTERM, handle_sigterm)

    try:
        p.wait()
    except KeyboardInterrupt:
        try:
            p.terminate()
        except OSError:
            pass
        p.wait()

    cleanup()

    sys.exit(p.returncode)


if __name__ == "__main__":
    cli()
