import pathlib
import shutil

import cv2
import numpy as np
import yaml

from .utils import (
    BlenderLineMask,
    get_blenderline_image,
    get_blenderline_masks,
    get_label_mapping,
)


def get_yolo_label(mask: BlenderLineMask, minarea: float) -> str | None:
    """Get YOLO bounding box label from BlenderLine generated pixel mask.

    Args:
        mask (BlenderLineMask): reference to mask with image ID, label ID, and image path.
        minarea (float): minimum area an object mask must have to be included.

    Returns:
        str | None: YOLO bounding box with class ID, or None if minarea is not exceeded.
    """
    # Read grayscale mask and binarize.
    mask_gray = cv2.imread(str(mask.path), cv2.IMREAD_GRAYSCALE)
    _, mask_binary = cv2.threshold(mask_gray, 127, 1, cv2.THRESH_OTSU)

    # Return None if mask is too small (< area_threshold).
    mask_height, mask_width = mask_gray.shape
    if mask_binary.sum() / (mask_width * mask_height) < minarea:
        return None

    # Compute bounding box relative to mask width and height.
    rows, cols = np.where(mask_binary == 1)
    xmin, xmax = cols.min(), cols.max()
    ymin, ymax = rows.min(), rows.max()

    xcenter = (xmin + xmax) / 2 / mask_width
    ycenter = (ymin + ymax) / 2 / mask_height
    width = (xmax - xmin) / mask_width
    height = (ymax - ymin) / mask_height

    # Return line in YOLO dataset format.
    return f"{mask.label} {xcenter} {ycenter} {width} {height}"


def run_convert_yolo_detection(
    source_path: pathlib.Path, target_path: pathlib.Path, minarea: float, remove: bool
) -> None:
    """Convert BlenderLine generated dataset to YOLO object detection dataset format.

    Args:
        source_path (pathlib.Path): absolute location of dataset to convert.
        target_path (pathlib.Path): absolute location of converted dataset.
        minarea (float): minimum area an object mask must have to be included.
        remove (bool): whether to remove the source dataset after converting.
    """
    # Create image and label subfolders.
    images_path = target_path / "images"
    labels_path = target_path / "labels"
    images_path.mkdir()
    labels_path.mkdir()

    # Load BlenderLine label mapping and prepopulate YOLO metadata. Paths to training,
    # validation, and testing data will be added when looping over the data splits.
    label_mapping = get_label_mapping(source_path)
    metadata = {
        "path": "/".join([".."] + list(target_path.parts[-2:])),
        "train": None,
        "val": None,
        "test": None,
        "names": label_mapping,
    }

    # Detect data splits from root BlenderLine dataset directory.
    split_paths = [path for path in source_path.iterdir() if path.is_dir()]

    for split_path in split_paths:
        # Create split folder within image and label directories
        images_split_path = images_path / split_path.name
        labels_split_path = labels_path / split_path.name
        images_split_path.mkdir()
        labels_split_path.mkdir()

        # Automatically detect split names as training, validation, or testing.
        # This may be done more cleanly, but YOLO expects slightly unusual names such
        # as "val" for the validation set, and putting restrictions on the split
        # naming possibilities is undesired. In most cases, this should work fine.
        if "train" in (split := split_path.name):
            metadata["train"] = f"images/{split}"
        if "val" in (split := split_path.name):
            metadata["val"] = f"images/{split}"
        if "test" in (split := split_path.name):
            metadata["test"] = f"images/{split}"

        instance_paths = [path for path in split_path.iterdir() if path.is_dir()]

        for instance_path in instance_paths:
            # Get generated image and copy it over to target dataset location.
            image = get_blenderline_image(instance_path)
            shutil.copy(image.path, images_split_path / f"{image.id}.png")

            # Get generated masks, convert them to YOLO bounding box format and merge
            # into one label file corresponding to image ID.
            masks = get_blenderline_masks(instance_path)
            labels = [
                label for mask in masks if (label := get_yolo_label(mask, minarea))
            ]
            with open(labels_split_path / f"{image.id}.txt", "w+") as file:
                file.write("\n".join(labels))

    # Create YOLO metadata file.
    with open(target_path / f"{source_path.name}.yaml", "w+") as file:
        yaml.dump(metadata, file, sort_keys=False)

    # Remove source dataset if desired.
    if remove:
        choice = input(f"Are you sure you want to remove source {source_path}? [y/N]: ")
        if choice == "y":
            shutil.rmtree(source_path)
        else:
            print("Source removal aborted.")
