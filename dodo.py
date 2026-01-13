"""Run or update the project. This file uses the `doit` Python package.

It works like a Makefile, but is Python-based. Run with: doit
List tasks: doit list
"""

#######################################
## Configuration and Helpers for PyDoit
#######################################

import shutil
from os import environ
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration from environment variables
DATA_DIR = Path(environ.get("DATA_DIR", "./_data"))
OUTPUT_DIR = Path(environ.get("OUTPUT_DIR", "./_output"))
OS_TYPE = environ.get("OS_TYPE", "nix")

# Create directories if they don't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


BASE_DIR = Path(__file__).parent

## Helpers for handling Jupyter Notebook tasks
environ["PYDEVD_DISABLE_FILE_VALIDATION"] = "1"


# fmt: off
## Helper functions for automatic execution of Jupyter notebooks
def jupyter_execute_notebook(notebook_path):
    return f"jupyter nbconvert --execute --to notebook --ClearMetadataPreprocessor.enabled=True --inplace {notebook_path}"

def jupyter_to_html(notebook_path, output_dir=OUTPUT_DIR):
    return (
        f"jupyter nbconvert --to html --log-level=ERROR "
        f"--output-dir='{output_dir}' {notebook_path}"
    )

def jupyter_to_md(notebook_path, output_dir=OUTPUT_DIR):
    """Requires jupytext"""
    return f"jupytext --to markdown --output-dir='{output_dir}' {notebook_path}"

def jupyter_clear_output(notebook_path):
    """Clear the output of a notebook"""
    return f"jupyter nbconvert --ClearOutputPreprocessor.enabled=True --ClearMetadataPreprocessor.enabled=True --inplace {notebook_path}"
# fmt: on


def mv(from_path, to_path):
    """Move a file to a folder"""
    from_path = Path(from_path)
    to_path = Path(to_path)
    to_path.mkdir(parents=True, exist_ok=True)
    if OS_TYPE == "nix":
        command = f"mv '{from_path}' '{to_path}'"
    else:
        command = f"move '{from_path}' '{to_path}'"
    return command


def copy_file(origin_path, destination_path, mkdir=True):
    """Create a Python action for copying a file."""

    def _copy_file():
        origin = Path(origin_path)
        dest = Path(destination_path)
        if mkdir:
            dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origin, dest)

    return _copy_file


##################################
## Begin rest of PyDoit tasks here
##################################


# Define notebook tasks - notebooks in src/ with _ipynb.py suffix
notebook_tasks = {
    "01_replicate_GSW_yield_curve_ipynb": {
        "path": "./src/01_replicate_GSW_yield_curve_ipynb.py",
        "file_dep": [],
        "targets": [],
    },
    "02_corp_bond_returns_ipynb": {
        "path": "./src/02_corp_bond_returns_ipynb.py",
        "file_dep": [],
        "targets": [],
    },
    "03_corp_bond_returns_ftsfr_HKM_ipynb": {
        "path": "./src/03_corp_bond_returns_ftsfr_HKM_ipynb.py",
        "file_dep": [],
        "targets": [],
    },
    "04_data_integration_tests_ipynb": {
        "path": "./src/04_data_integration_tests_ipynb.py",
        "file_dep": [],
        "targets": [],
    },
    "05_factor_regression_example_ipynb": {
        "path": "./src/05_factor_regression_example_ipynb.py",
        "file_dep": [],
        "targets": [],
    },
}


# fmt: off
def task_run_notebooks():
    """Preps the notebooks for presentation format.
    Execute notebooks if the script version of it has been changed.
    Also copies notebooks to docs_src/examples/ for Sphinx documentation.
    """
    for notebook in notebook_tasks.keys():
        pyfile_path = Path(notebook_tasks[notebook]["path"])
        notebook_path = pyfile_path.with_suffix(".ipynb")
        yield {
            "name": notebook,
            "actions": [
                """python -c "import sys; from datetime import datetime; print(f'Start """ + notebook + """: {datetime.now()}', file=sys.stderr)" """,
                f"jupytext --to notebook --output {notebook_path} {pyfile_path}",
                jupyter_execute_notebook(notebook_path),
                jupyter_to_html(notebook_path),
                mv(notebook_path, OUTPUT_DIR / "_notebook_build"),
                # Copy executed notebook to docs_src/examples/ for Sphinx
                copy_file(
                    OUTPUT_DIR / "_notebook_build" / f"{notebook}.ipynb",
                    BASE_DIR / "docs_src" / "examples" / f"{notebook}.ipynb",
                ),
                """python -c "import sys; from datetime import datetime; print(f'End """ + notebook + """: {datetime.now()}', file=sys.stderr)" """,
            ],
            "file_dep": [
                pyfile_path,
                *notebook_tasks[notebook]["file_dep"],
            ],
            "targets": [
                OUTPUT_DIR / f"{notebook}.html",
                OUTPUT_DIR / "_notebook_build" / f"{notebook}.ipynb",
                BASE_DIR / "docs_src" / "examples" / f"{notebook}.ipynb",
                *notebook_tasks[notebook]["targets"],
            ],
            "clean": True,
        }
# fmt: on


sphinx_targets = [
    "./docs/index.html",
]


def clean_jupyter_execute():
    """Remove the jupyter_execute directory created by myst-nb."""
    jupyter_execute_dir = BASE_DIR / "jupyter_execute"
    if jupyter_execute_dir.exists():
        shutil.rmtree(jupyter_execute_dir)


def create_nojekyll():
    """Create .nojekyll file for GitHub Pages."""
    (BASE_DIR / "docs" / ".nojekyll").touch()


def task_compile_sphinx_docs():
    """Compile Sphinx Docs"""
    notebook_scripts = [
        Path(notebook_tasks[notebook]["path"]) for notebook in notebook_tasks.keys()
    ]
    file_dep = [
        "./docs_src/conf.py",
        "./docs_src/index.md",
        *notebook_scripts,
    ]

    return {
        "actions": [
            "sphinx-build -b html docs_src docs",
            clean_jupyter_execute,  # Clean up myst-nb temp directory
            create_nojekyll,  # Create .nojekyll for GitHub Pages
        ],
        "targets": sphinx_targets,
        "file_dep": file_dep,
        "task_dep": [
            "run_notebooks",
        ],
        "clean": True,
    }


def task_test():
    """Run pytest"""
    return {
        "actions": ["pytest tests/ -v"],
        "file_dep": list(Path("src/finm").rglob("*.py")),
        "verbosity": 2,
    }


def task_build_package():
    """Build the Python package using hatch"""
    return {
        "actions": ["hatch build"],
        "file_dep": [
            "pyproject.toml",
            *list(Path("src/finm").rglob("*.py")),
        ],
        "targets": [
            "dist/finm-0.1.0.tar.gz",
            "dist/finm-0.1.0-py3-none-any.whl",
        ],
        "clean": True,
    }
