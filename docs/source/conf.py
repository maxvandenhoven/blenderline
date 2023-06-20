import os
import sys
sys.path.insert(0, os.path.abspath("../.."))

# Project information
project = "BlenderLine"
author = "Max van den Hoven"
copyright = "2023, Max van den Hoven"

# General configuration
extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx_design", 
    "sphinx_copybutton",
]
templates_path = ["_templates"]

# Options for HTML output
html_theme = "furo"
html_favicon = "_static/favicons/favicon.ico"
html_css_files = ["blenderline.css"]
html_static_path = ["_static"]
html_theme_options = {
    "sidebar_hide_name": True,
    "light_logo": "logos/logo-full-light.svg",
    "dark_logo": "logos/logo-full-dark.svg",
    "light_css_variables": {
        # API reference styling
        "color-api-background": "rgba(215, 79, 100, 0.25)",
        "color-api-background-hover": "rgba(215, 79, 100, 0.25)",
        "color-api-keyword": "black",
        "color-api-pre-name": "black",
        "color-api-name": "black",        
        "color-api-paren": "black",
        "color-api-overall": "black",
        "color-highlight-on-target": "rgba(217, 152, 85, 0.5)",
    },
    "dark_css_variables": {
        # API reference styling
        "color-api-background": "rgba(215, 79, 100, 0.5)",
        "color-api-background-hover": "rgba(215, 79, 100, 0.5)",
        "color-api-keyword": "white",
        "color-api-pre-name": "white",
        "color-api-name": "white",        
        "color-api-paren": "white",
        "color-api-overall": "white",
        "color-highlight-on-target": "rgba(217, 152, 85, 0.75)",
    },
}

# Autodoc settings
autodoc_typehints = "description"
autodoc_class_signature = "separated"