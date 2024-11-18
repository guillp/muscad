"""Sphinx configuration."""

from datetime import UTC, datetime

project = "MuSCAD"
author = "Guillaume Pujol"
copyright = f"{datetime.now(tz=UTC).year}, {author}"  # noqa: A001
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "sphinx_rtd_theme",
]
autodoc_typehints = "description"
html_theme = "sphinx_rtd_theme"
