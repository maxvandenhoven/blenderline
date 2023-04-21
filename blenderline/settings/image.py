##########################################################################################
# Imports
##########################################################################################
import json
import pathlib

from blenderline.collections import BackgroundCollection, HDRCollection, ItemCollection
from blenderline.entries import BackgroundEntry, HDREntry, ItemEntry
from blenderline.generators import ImageDatasetGenerator
from blenderline.managers import BackgroundManager, HDRManager, SceneManager, ItemManager


##########################################################################################
# Settings object
##########################################################################################
class ImageDatasetSettings:
    def __init__(
        self, 
        base_dir: str | pathlib.Path, 
        filepath: str | pathlib.Path
    ) -> None:
        """ TODO

        Args:
            base_dir (pathlib.Path): Path to project directory.
            filename (pathlib.Path): Path to JSON config file.
        """ 
        # Save base directory and load JSON config object.
        self.base_dir = base_dir
        with open(filepath, mode="rt", encoding="utf-8") as file:
            self.settings: dict = json.load(file)


    def get(self, key: str, default = None):
        """ Get nested value from settings dictionary using dot notation to specify
            a path of keys to follow. E.g., "scene.path". Intermediate keys will return
            an empty dictionary of not present, so the function will always follow the
            entire key path.

        Args:
            key (str): dot-separated path of keys to follow
            default (_type_, optional): default value to return if key does not exist. 
                Note that this is also triggered if an intermediary key is not present.
                Defaults to None.
        """        
        parts = key.split(".")

        # If only one key, perform normal dictionary get on settings dictionary.
        if len(parts) == 1:
            return self.settings.get(parts[0], default)
        # If two keys, get first key first with empty dictionary as default.
        elif len(parts) == 2:
            return self.settings.get(parts[0], {}).get(parts[1], default)
        # For more than three keys (n), get the first n-1 keys with an empty dictionary
        # as default value.
        else:
            current_dict = self.settings
            for part in parts[:-1]:
                current_dict = current_dict.get(part, {})
            return current_dict.get(parts[-1], default)


    def get_hdr_collection(self) -> HDRCollection:
        """ Create HDR collection from registered HDR backgrounds in settings.

        Returns:
            HDRCollection: collection of HDR backgrounds.
        """        
        hdr_collection = HDRCollection()

        # Get list of registered HDR dictionaries.
        hdrs: list[dict] = self.get("hdrs.entries", [])

        for hdr in hdrs:
            # Validate registered HDR dict by checking for a relative filepath.
            if "path" not in hdr:
                raise Exception("Configure path to HDR asset")
            
            # Build registered HDR object from dict and register it to the collection.
            hdr_collection.register(
                HDREntry(
                    filepath=self.base_dir / hdr["path"],
                    relative_frequency=hdr.get("relative_frequency", 1)
                )
            )

        return hdr_collection
    

    def get_background_collection(self) -> BackgroundCollection:
        """ Create background collection from registered backgrounds in settings.

        Returns:
            BackgroundCollection: collection of backgrounds.
        """   
        background_collection = BackgroundCollection()

        # Get list of registered background dictionaries.   
        backgrounds: list[dict] = self.get("backgrounds.entries", []) 

        for background in backgrounds:
            # Validate registered HDR dict by checking for a relative filepath.
            if "path" not in background:
                raise Exception("Configure path to background asset")
            
            # Build registered HDR object from dict and register it to the collection.
            background_collection.register(
                BackgroundEntry(
                    filepath=self.base_dir / background["path"],
                    relative_frequency=background.get("relative_frequency", 1)
                )
            )

        return background_collection 
    

    def get_item_collection(self) -> ItemCollection:
        """ Create item collection from registered items in settings.

        Returns:
            ItemCollection: collection of items.
        """       
        item_collection = ItemCollection()

        # Get list of registered item dictionaries.
        items: list[dict] = self.get("items.entries", [])

        for item in items:
            # Validate registered item dict by checking for a relative filepath, label,
            # object name and margin.
            if "path" not in item:
                raise Exception("Configure path to item asset")
            if "label" not in item:
                raise Exception("Configure item label")
            if "object_name" not in item:
                raise Exception("Configure name of object in .blend file")
            if "min_margin_distance" not in item:
                raise Exception("Configure minimum distance to other items")
            if "max_lateral_distance" not in item:
                raise Exception("Configure maximum distance from path center line")
            
            # Build registered HDR object from dict and register it to the collection.
            item_collection.register(
                ItemEntry(
                    filepath=self.base_dir / item["path"],
                    label=item["label"],
                    object_name=item["object_name"],
                    min_margin_distance=item["min_margin_distance"],
                    max_lateral_distance=item["max_lateral_distance"],
                    relative_frequency=item.get("relative_frequency", 1)
                )
            )

        return item_collection 

    
    def get_scene_manager(self) -> SceneManager:
        """ Create scene manager using parameters configured in settings.

        Returns:
            SceneManager: scene manager object.
        """        
        # Validate scene settings by checking for a relative filepath.
        if not self.get("scene.path"):
            raise Exception("Configure path to scene asset")

        # Return scene manager with specified parameters, falling back to defaults if not
        # specified.
        return SceneManager(
            filepath=self.base_dir / self.settings["scene"]["path"],
            camera_object_name=self.get("scene.camera_object_name", "camera"),
            render_samples=self.get("scene.render_samples", 1024),
            render_use_cuda=self.get("scene.render_use_cuda", False),
            render_denoising=self.get("scene.render_denoising", True),
            render_resolution=self.get("scene.render_resolution", [512, 512]),
        )
    

    def get_hdr_manager(self) -> HDRManager:
        """ Create HDR background manager using parameters configured in settings.

        Returns:
            HDRManager: HDR manager object.
        """        
        return HDRManager(
            hdr_collection=self.get_hdr_collection()
        )
    

    def get_background_manager(self) -> BackgroundManager:
        """ Create background manager using parameters configured in settings.

        Returns:
            BackgroundManager: background manager object.
        """        
        return BackgroundManager(
            background_object_name=self.get("scene.background_object_name", "background"),
            background_collection=self.get_background_collection()
        )
    

    def get_item_manager(self) -> ItemManager:
        """ Create item manager using parameters configured in settings.

        Returns:
            ItemManager: item manager object.
        """
        return ItemManager(
            path_object_name=self.get("items.path_object_name", "path"),
            spawn_probability=self.get("items.spawn_probability", 0.5),
            max_tries=self.get("items.max_tries", 3),
            max_items=self.get("items.max_items", 5),
            item_collection=self.get_item_collection()
        )
    

    def get_dataset_generator(self) -> ImageDatasetGenerator:
        """ Create image dataset generator using parameters configured in settings.

        Returns:
            ImageDatasetGenerator: dataste generator object.
        """      
        # Create object using settings.  
        image_dataset_generator = ImageDatasetGenerator(
            name=self.get("dataset.name", "dataset"),
            base_dir=self.base_dir,
            scene_manager=self.get_scene_manager(),
            hdr_manager=self.get_hdr_manager(),
            background_manager=self.get_background_manager(),
            item_manager=self.get_item_manager()
        )

        # Register all splits.
        for split_dict in self.get("dataset.splits", []):
            if "name" not in split_dict or "size" not in split_dict:
                raise Exception("Invalid split configured. Specify name and size keys.")
            
            image_dataset_generator.register_split(split_dict["name"], split_dict["size"])

        return image_dataset_generator
    
