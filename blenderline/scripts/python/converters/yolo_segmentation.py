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


def get_yolo_segmentation_label(
    mask: BlenderLineMask, minarea: float, eps_factor: float = None
) -> str | None:
    """Get YOLO segmentation mask label from BlenderLine generated pixel mask.

    Args:
        mask (BlenderLineMask): reference to mask with image ID, label ID, and image path.
        minarea (float): minimum area an object mask must have to be included.
        eps_factor (float, optional): factor used to smooth segmentation mask. Higher
            values lead to rougher masks, and vice versa. Defaults to None.

    Returns:
        str | None: YOLO segmentation mask with class ID, or None if minarea is not
            exceeded.
    """
    # Read grayscale mask and binarize.
    mask_gray = cv2.imread(str(mask.path), cv2.IMREAD_GRAYSCALE)
    _, mask_binary = cv2.threshold(mask_gray, 127, 1, cv2.THRESH_OTSU)

    # Find all contours in mask image. There may be more than one contour, e.g., if the
    # object of interest is occluded.
    contours, _ = cv2.findContours(mask_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Object area is computed by summing the area of all contour parts, in order to
    # prevent half-labeled objects. Return None if mask is too small (< area_threshold).
    mask_height, mask_width = mask_gray.shape
    total_contour_area = sum(cv2.contourArea(contour) for contour in contours)
    if total_contour_area / (mask_width * mask_height) < minarea:
        return None

    label_lines = []
    for contour in contours:
        # OpenCV often generates high-resolution boundaries, which may not be desired for
        # segmentation tasks. The contours are therefore optionally simplified using the
        # Douglas-Peucker algorithm, with the precision detemrined by multiplying the
        # specified eps_factor with the contour perimeter. The approxPolyDP function
        # takes in integer coordinates, meaning eps_factor cannot be specified in the
        # normalized coordinate space.
        if eps_factor:
            epsilon = eps_factor * cv2.arcLength(contour, closed=True)
            contour = cv2.approxPolyDP(contour, epsilon, closed=True)

        # Normalize contour coordinates by dividing by mask dimensions (using numpy
        # broadcasting rules with compatible trailing dimensions (1, 2)).
        contour = contour / np.array([[mask_width, mask_height]])

        # Reshape contour coordinates to sequential array and prepend mask label ID for
        # full label line.
        label_line = mask.label + " " + " ".join(map(str, contour.reshape(-1)))
        label_lines.append(label_line)

    # Split label lines by \n so that occluded objects get multiple lines in the label.
    return "\n".join(label_lines)


def run_convert_yolo_segmentation(
    source_path: pathlib.Path,
    target_path: pathlib.Path,
    minarea: float = 0.005,
    remove: bool = False,
    eps_factor: float = None,
    **kwargs,
) -> None:
    """Convert BlenderLine generated dataset to YOLO segmentation dataset format.

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
                label
                for mask in masks
                if (label := get_yolo_segmentation_label(mask, minarea, eps_factor))
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
