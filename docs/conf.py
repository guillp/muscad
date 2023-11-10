"""Sphinx configuration."""
from datetime import datetime

project = "MuSCAD"
author = "Guillaume Pujol"
copyright = f"{datetime.utcnow().year}, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "sphinx_rtd_theme",
]
autodoc_typehints = "description"
html_theme = "sphinx_rtd_theme"