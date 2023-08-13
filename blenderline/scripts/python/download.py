import io
import os
import pathlib
import shutil
import tempfile
import zipfile

import requests

REPO_URL = "https://github.com/maxvandenhoven/blenderline/archive/refs/heads/main.zip"


def run_download(name: str, target: str = None) -> None:
    # Get absolute path to target directory if given, else, set target directory to
    # current working directory.
    if target:
        target_path = pathlib.Path(os.path.abspath(target)) / name
    else:
        target_path = pathlib.Path(os.getcwd()) / name

    # Download entire BlenderLine repository zip, as it is not possible to gracefully
    # download subfolder from repository. Example projects are not hosted separately,
    # as Google Drive and Dropbox do not allow for easy downloads using Python, and to
    # keep from having to synchronize the BlenderLine repository with 3rd party platforms.
    response = requests.get(REPO_URL)

    if not response.ok:
        raise Exception(f"Repository request failed ({response.status_code})")

    # Extract files related to desired example project to temporary folder and copy to
    # desired target location from there. A temporary folder is required, as the zipfile
    # module does not allow simultaneous extraction and renaming of subfiles/folders.
    with tempfile.TemporaryDirectory() as temp_folder:
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            for file in zip_file.namelist():
                if file.startswith(f"blenderline-main/examples/{name}"):
                    zip_file.extract(file, temp_folder)
        source_path = os.path.join(temp_folder, f"blenderline-main/examples/{name}")
        shutil.copytree(source_path, target_path)
