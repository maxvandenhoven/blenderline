from setuptools import find_packages, setup

setup(
    name="blenderline",
    version="0.0.1",
    description="A pipeline for generating synthetic production line images",
    packages=find_packages(exclude=["examples*", "data*"]),
    url="https://github.com/MaxvandenHoven/blenderline",
    author="Max van den Hoven",
    author_email="max.hoven@gmail.com",
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy==1.24.2 ",
        "blender-stubs==3.12.27",
        "bpy==3.5.0",
    ],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "blenderline = blenderline.command_line:cli",
        ],
    },
)
