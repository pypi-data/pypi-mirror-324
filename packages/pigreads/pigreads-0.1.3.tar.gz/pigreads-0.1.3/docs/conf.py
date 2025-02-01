from __future__ import annotations

import importlib.metadata
from typing import Any

project = "Pigreads"
copyright = "2024, Desmond Kabus"
author = "Desmond Kabus"
version = release = importlib.metadata.version("pigreads")

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
]

source_suffix = [".rst", ".md"]
exclude_patterns = [
    "_build",
    "**.ipynb_checkpoints",
    "Thumbs.db",
    ".DS_Store",
    ".env",
    ".venv",
]

html_theme = "furo"

html_theme_options: dict[str, Any] = {
    "source_repository": "https://gitlab.com/pigreads/pigreads",
    "source_branch": "main",
    "source_directory": "docs/",
}

myst_enable_extensions = [
    "colon_fence",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable", None),
}

nitpick_ignore = [
    ("py:class", "numpy.int32"),  # TODO: remove when possible
    ("py:class", "numpy.int64"),  # TODO: remove when possible
    ("py:class", "numpy.float32"),  # TODO: remove when possible
    ("py:class", "numpy.float64"),  # TODO: remove when possible
    ("py:class", "_io.StringIO"),
    ("py:class", "_io.BytesIO"),
]

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "no-value": True,
}

always_document_param_types = True
typehints_fully_qualified = False
typehints_defaults = "braces-after"
typehints_document_rtype = True
