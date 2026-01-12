"""Sphinx configuration for finm documentation."""

import sys
from pathlib import Path

# Path setup for autodoc2
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# -- Project information -----------------------------------------------------
project = "finm"
copyright = "2024, University of Chicago Financial Mathematics Program"
author = "University of Chicago Financial Mathematics Program"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
extensions = [
    "autodoc2",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "myst_nb",
    "sphinx_design",
    "sphinx_copybutton",
]

# autodoc2 configuration
autodoc2_packages = [
    "../src/finm",
]
autodoc2_render_plugin = "myst"
autodoc2_hidden_objects = ["dunder", "private", "inherited"]
autodoc2_sort_names = True
autodoc2_class_docstrings = "both"

# MyST configuration
myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]
myst_url_schemes = ["mailto", "http", "https"]

# Notebook execution
nb_execution_mode = "off"  # Notebooks are pre-executed by dodo.py
nb_execution_allow_errors = False
nb_execution_timeout = 300

# Source suffix
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "myst-nb",
    ".myst": "myst-nb",
    ".ipynb": "myst-nb",
}

# Templates and static files
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_book_theme"
html_theme_options = {
    "navigation_with_keys": True,
    "search_bar_text": "Search documentation...",
    "repository_url": "https://github.com/uchicago-finmath/finm",
    "repository_branch": "main",
    "path_to_docs": "docs_src",
    "use_repository_button": True,
    "use_issues_button": True,
    "home_page_in_toc": True,
    "show_navbar_depth": 2,
    "show_toc_level": 3,
}

html_title = "finm Documentation"
html_static_path = ["_static"]
html_logo = "_static/logo.png"

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
}

# Suppress warnings
suppress_warnings = ["myst.domains", "autodoc2.dup_item"]
