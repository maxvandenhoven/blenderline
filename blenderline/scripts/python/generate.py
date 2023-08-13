import os
import pathlib
import signal
import subprocess
import sys

blenderline_dir = pathlib.Path(__file__).parent.parent.parent.parent
sys.path.append(str(blenderline_dir))


def run_generate(config: str, target: str = None, blender: str = None) -> None:
    # Get absolute path to configuration file and check that it is valid, i.e., exists
    # and is a JSON file.
    config_path = pathlib.Path(os.path.abspath(config))
    if not config_path.is_file() or config_path.suffix != ".json":
        raise Exception("Please specify a valid configuration file.")

    # Get absolute path to target directory if given, else, set target directory to
    # current working directory. Existence need not be checked, as Blender creates
    # all intermediate folders in the rendering process.
    if target:
        target_path = pathlib.Path(os.path.abspath(target))
    else:
        target_path = pathlib.Path(os.getcwd())

    # Append Blender start command to path if given, else, assume Blender start command
    # is available on path and can be called using `blender`. No verification is performed
    # on the given path, as this is likely platform-dependent.
    if blender:
        blender_path = pathlib.Path(blender) / "blender"
    else:
        blender_path = "blender"

    # Get absolute path to generate script to be executing in Blender context.
    script_path = (
        blenderline_dir / "blenderline" / "scripts" / "blender" / "generate.py"
    )

    # Start Blender process.
    blender_process = subprocess.Popen(
        [
            str(blender_path),
            "--background",
            "--python",
            str(script_path),
            "--",
            "--config",
            str(config_path),
            "--target",
            str(target_path),
        ]
    )

    # Handle termination of the subprocess
    signal.signal(signal.SIGTERM, lambda _signum, _frame: blender_process.terminate())

    try:
        blender_process.wait()
    except KeyboardInterrupt:
        try:
            blender_process.terminate()
        except OSError:
            pass
        blender_process.wait()

    sys.exit(blender_process.returncode)
