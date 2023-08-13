import os
import pathlib

from blenderline.scripts.python.converters import (
    run_convert_yolo_detection,
    run_convert_yolo_segmentation,
)

CONVERTERS = {
    "yolo_detection": run_convert_yolo_detection,
    "yolo_segmentation": run_convert_yolo_segmentation,
}


def run_convert(
    format: str, source: str, target: str, minarea: float, remove: bool, **kwargs
) -> None:
    # Get absolute path to source folder and check that it is valid, i.e., exists and
    # contains a label_mapping.json file.
    source_path = pathlib.Path(os.path.abspath(source))
    if not source_path.is_dir() or "label_mapping.json" not in os.listdir(source_path):
        raise Exception(
            "Please specify a valid source directory in BlenderLine format."
        )

    # Get absolute path to target folder and check that it is valid, i.e., does not exist
    # or is empty. Also check if the target directory is not equal to the source directory
    # This is probably not needed however, as the source directory is likely not empty.
    target_path = pathlib.Path(os.path.abspath(target))
    if target_path == source_path:
        raise Exception("Please choose a different target directory than the source.")
    if target_path.exists() and any(target_path.iterdir()):
        raise Exception("Please make sure that the target directory is empty.")

    target_path.mkdir(parents=True, exist_ok=True)

    # Run converter corresponding to specified target format.
    convertor = CONVERTERS[format]
    convertor(source_path, target_path, minarea, remove, **kwargs)
