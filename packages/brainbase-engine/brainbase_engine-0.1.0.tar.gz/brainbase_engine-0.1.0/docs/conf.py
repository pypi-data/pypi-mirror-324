# Configuration file for Sphinx documentation builder

import os
import sys

sys.path.insert(0, os.path.abspath("../src"))

project = "Brainbase Python SDK"
copyright = "2024, Brainbase Labs"
author = "Brainbase Labs"
release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_rtd_theme",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
