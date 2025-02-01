import sys
from pathlib import Path
from typing import Optional, Union, List

import nbformat
from nbformat.reader import NotJSONError

import dreamml
from dreamml.logging import get_logger

_logger = get_logger(__name__)


def update_notebooks(notebooks: List[Path], version=None):
    for notebook_path in notebooks:
        try:
            update_notebook_mpack_kernel(notebook_path, version)
        except NotJSONError as e:
            _logger.exception(e)


def gather_notebooks(path: Union[Path, str]):
    path = Path(path)

    notebook_paths = [
        notebook_path
        for notebook_path in path.glob("**/*.ipynb")
        if not any(
            part.startswith(".") for part in notebook_path.relative_to(path).parts
        )
        and not notebook_path.stem.startswith("_")
    ]

    return notebook_paths


def update_notebook_mpack_kernel(notebook_path, version=None):
    # Read the notebook content
    with open(notebook_path, "r", encoding="utf-8") as notebook_file:
        notebook_node = nbformat.read(notebook_file, as_version=4)

    if version is None:
        version = dreamml.__version__

    kernelspec = get_mpack_kernelspec_by_version(version)

    notebook_node["metadata"]["kernelspec"]["display_name"] = kernelspec["display_name"]
    notebook_node["metadata"]["kernelspec"]["name"] = kernelspec["name"]

    with open(notebook_path, "w", encoding="utf-8") as notebook_file:
        nbformat.write(notebook_node, notebook_file)


def get_mpack_kernelspec_by_version(version: str):
    version_joined = version.replace(".", "")

    kernelname = f"dmlmpack{version_joined}"

    python_string = f"py{sys.version_info[0]}.{sys.version_info[1]}"

    kernelspec = {
        "display_name": f"{python_string}_{kernelname}_{version}",
        "language": "python",
        "name": kernelname,
    }

    return kernelspec