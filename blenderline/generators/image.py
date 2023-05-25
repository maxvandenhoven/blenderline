import json
import pathlib
from dataclasses import dataclass

from blenderline.managers import (
    BackgroundManager,
    HDRManager,
    ItemManager,
    SceneManager,
)


@dataclass(frozen=True, eq=True)
class Split:
    """Split in dataset."""

    name: str
    size: int


@dataclass(frozen=True, eq=True)
class Label:
    """Label in dataset"""

    label: int
    label_name: str


class ImageDatasetGenerator:
    """Generator for image datasets."""

    def __init__(
        self,
        name: str,
        target: pathlib.Path,
        scene_manager: SceneManager,
        hdr_manager: HDRManager,
        background_manager: BackgroundManager,
        item_manager: ItemManager,
    ) -> None:
        """Create dataset generator.

        Args:
            name (str): name of dataset. Output folder will be target/<name>/<split>.
            target (pathlib.Path): base directory in which to put data.
            scene_manager (SceneManager): scene manager.
            hdr_manager (HDRManager): HDR background manager.
            background_manager (BackgroundManager): background manager.
            item_manager (ItemManager): item manager.
        """
        # Save object attributes.
        self.name = name
        self.target = target
        self.scene_manager = scene_manager
        self.hdr_manager = hdr_manager
        self.background_manager = background_manager
        self.item_manager = item_manager

        # Keep track of registered splits and labels.
        self.registered_splits: list[Split] = list()
        self.registered_labels: set[Label] = set()

    def register_split(self, name: str, size: int) -> None:
        """Register dataset split to generate

        Args:
            name (str): name of split to generate within dataset name output folder.
            size (int): number of images to generate.
        """
        self.registered_splits.append(Split(name, size))

    def register_label(self, label: int, label_name: str) -> None:
        """Register dataset label to generate

        Args:
            label (int): label index found in mask filenames.
            label_name (str): semantic name for label index.
        """
        self.registered_labels.add(Label(label, label_name))

    def initialize(self) -> None:
        self.scene_manager.initialize()
        self.hdr_manager.initialize()
        self.background_manager.initialize()
        self.item_manager.initialize()

    def generate_dataset(self) -> None:
        for split in self.registered_splits:
            for i in range(split.size):
                # Randomly sample (HDR) background.
                self.hdr_manager.sample()
                self.background_manager.sample()

                # Sample number of items and assign pass indices
                self.item_manager.sample()
                self.item_manager.assign_pass_indices()

                # Render image and segmentation masks
                self.scene_manager.render(
                    output_folder=self.target / self.name / split.name / str(i),
                    item_references=self.item_manager.item_references,
                )

                # Clear items for next iteration
                self.item_manager.clear()

        # Write label mapping
        with open(self.target / self.name / "label_mapping.json", mode="+wt") as file:
            label_mapping = {
                label.label: label.label_name for label in self.registered_labels
            }
            json.dump(label_mapping, file)
