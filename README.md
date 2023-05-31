# BlenderLine

[![GPLv3](https://img.shields.io/static/v1?message=GPLv3&color=blue&label=License&style=flat)](https://www.gnu.org/licenses/gpl-3.0)
[![Blender](https://img.shields.io/static/v1?message=3.10%2B&logo=python&color=blue&logoColor=white&label=Python&style=flat)](https://www.python.org/)
[![Blender](https://img.shields.io/static/v1?message=3.4%2B&logo=blender&color=orange&logoColor=white&label=Blender&style=flat)](https://www.blender.org/)
[![GPLv3](https://img.shields.io/static/v1?message=black&color=black&label=Code%20style&style=flat)](https://github.com/psf/black)


## 1. Table of Contents
<details>
<summary> Table of Contents </summary>

- [1. Table of Contents](#1-table-of-contents)
- [2. Description](#2-description)
- [3. Features](#3-features)
- [4. Installation](#4-installation)
- [5. Usage](#5-usage)
- [6. Roadmap](#6-roadmap)

</details>


## 2. Description
Coming soon!


## 3. Features
- **Flexible**: BlenderLine imposes as little constraints on your 3D modeling workflow as possible, giving you the freedom to model your production line as you see fit.
- **Declerative**: Instead of having to write the generation code yourself, BlenderLine enables you to define the desired behavior of objects on your production line using declarative configuration files. 
- **Powerful**: Despite using declarative configuration files, BlenderLine is powerful enough to support a wide variety of use cases, ranging from narrow bottle counting lines (see `examples/example_beer`) to wide conveyor belts (example planned).
- **Convenient**: BlenderLine includes tools to easily convert generated datasets into common computer vision dataset formats:
  - `yolo_detection`
  - `yolo_segmentation` (planned)
  - `coco_detection` (planned)
  - `coco_segmentation` (planned)


## 4. Installation
The simplest way to install BlenderLine is using pip:
```
pip install blenderline
```

Alternatively, you can choose to clone the repository to make a local pip installation:
```
git clone https://github.com/maxvandenhoven/blenderline
cd blenderline
pip install -e .
```

Note that, by default, BlenderLine assumes that Blender is installed and available on your system `PATH`, meaning that the Blender CLI can be invoked using only the `blender` command. The platform-dependent documentation below can help you add Blender to your system `PATH`:
- [Windows](https://docs.blender.org/manual/en/latest/advanced/command_line/launch/windows.html)
- [MacOS](https://docs.blender.org/manual/en/latest/advanced/command_line/launch/macos.html)
- [Linux](https://docs.blender.org/manual/en/latest/advanced/command_line/launch/linux.html)

Alternatively, you can use the optional `--blender` argument in `blenderline generate` to specify where Blender is installed on your system.

## 5. Usage
##### Generate Images
The `blenderline generate` command is used to generate a dataset of synthetic images from a configuration file. You can test BlenderLine with the provided `examples/example_beer/images.json` example as follows:
```
blenderline generate --config examples/example_beer/images.json --target data/raw
```

This will generate a dataset with the following structure:
```
data/
└─ raw/
   └─ example_beer/
      ├─ train/
      │  ├─ 0/
      │  │  ├─ image__f0825a6262fc__0001.png
      │  │  ├─ mask__0__8acdea079f10__0001.png
      │  │  ├─ mask__1__0181a303d637__0001.png
      │  │  └─ ...
      │  └─ 1/
      │     ├─ image__7abe7f02c7d9__0001.png
      │     ├─ mask__1__19abef8a5cef__0001.png
      │     ├─ mask__1__d980d4a83682__0001.png
      │     └─ ...
      ├─ valid/
      │  ├─ 0/...
      │  └─ 1/...
      └─ label_mapping.json

```

While not strictly necessary, setting `--target data/raw` will create a folder structure that allows you to track different versions of the data, e.g., after using the `blenderline convert` command. 

Note that the dataset root folder (here named `example_beer`) contains subfolders for different splits defined in the configuration file. Each split contains a numbered list of instance folders, each containing a rendered image and a set of masks. An example instance might look as follows:
![Example instance](/img/example-instance.png)

Image and mask files use the following naming convention:
```
image__<random image ID>__0001.png
mask__<class ID>__<random mask ID>__0001.png
```

###### Convert Dataset 
Coming soon!



## 6. Roadmap
| **Version**      | **Features**                                          |
|------------------|-------------------------------------------------------|
| v0.1.0 (current) | Image generation pipeline + CLI interface             |
| v0.2.0           | YOLO detection conversion pipeline + CLI interface    |
| v0.3.0           | Documentation + tutorial + second example             |
| v0.4.0           | YOLO segmentation conversion pipeline + CLI interface |
| v0.5.0           | COCO detection conversion pipeline + CLI interface    |
| v0.6.0           | COCO segmentation conversion pipeline + CLI interface |