##########################################################################################
# Imports
##########################################################################################
import json
import pathlib

from blenderline.entries import BackgroundEntry, HDREntry
from blenderline.collections import BackgroundCollection, HDRCollection


##########################################################################################
# Settings object
##########################################################################################
class ImageGenerationSettings:
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
    

    def get_hdr_collection(self) -> HDRCollection:
        """ Create HDR collection from registered HDR backgrounds in settings.

        Returns:
            HDRCollection: collection of HDR backgrounds.
        """        
        hdr_collection = HDRCollection()

        # Get list of registered HDR dictionaries, defaulting to empty list if not given.
        hdrs: list[dict] = self.settings.get("hdrs", {}).get("entries", [])

        for hdr in hdrs:
            # Validate registered HDR dict by checking for a relative filepath.
            if "path" not in hdr:
                raise Exception("Configure path to HDR asset")
            
            # Build registered HDR object from dict and register it to the collection.
            hdr_collection.register(HDREntry(
                filepath=self.base_dir / hdr["path"],
                relative_freq=hdr.get("relative_frequency", 1)
            ))

        return hdr_collection
    

    def get_background_collection(self) -> BackgroundCollection:
        """ Create background collection from registered backgrounds in settings.

        Returns:
            BackgroundCollection: collection of backgrounds.
        """   
        background_collection = BackgroundCollection()

        # Get list of registered background dictionaries, default to empty list if not given.   
        backgrounds: list[dict] = self.settings.get("backgrounds", {}).get("entries", []) 

        for background in backgrounds:
            # Validate registered HDR dict by checking for a relative filepath.
            if "path" not in background:
                raise Exception("Configure path to background asset")
            
            # Build registered HDR object from dict and register it to the collection.
            background_collection.register(BackgroundEntry(
                filepath=self.base_dir / background["path"],
                relative_freq=background.get("relative_frequency", 1)
            ))

        return background_collection 
    