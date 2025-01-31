# SPDX-FileCopyrightText: © 2024 nosludge <https://github.com/nosludge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Load configuration from config file(s)."""

from __future__ import annotations

import pathlib
import tomllib

from . import _load


def config(
    name: str,
    path: pathlib.Path | str | None = None,
    directory: pathlib.Path | str | None = None,
    vcs: bool = True,  # noqa: FBT001, FBT002
) -> dict:
    """Read `pyproject.toml` configuration file.

    The following paths are checked in order (first found used):
    - `path` (section `[tool.{name}]` or data in the whole file)
    - `.{name}.toml` in the current directory
    - `pyproject.toml` in the current directory
    - `.{name}.toml` in the project root (if `vcs=True`)
    as defined by `git`, `hg`, or `svn`
    - `pyproject.toml` in the project root (if `vcs=True`)
    as defined by `git`, `hg`, or `svn`

    Warning:
        Automatically returns __only__ the relevant configuration
        of the linter.

    Args:
        name:
            The name of the tool to search for in the configuration file.
        path:
            Explicitly provided path to the configuration file, if any.
            If not given, `tooload` will try to guess based on `directory`
            and `vcs`.
        directory:
            The directory to search for the configuration file.
            If not provided, the current working directory is used.
        vcs:
            Whether the version control system directories should be
            searched for when localizing the project root.

    Raises:
        ConfigMissingError:
            If the `path` is specified, but the file does not exist.
        TomlDecodeError:
            If any of the files were found, but could not be read.

    Returns:
        Configuration dictionary of the tool or an empty dictionary.

    """
    if (cfg := _load.specified_path(name, path)) is not None:
        return cfg

    if directory is None:
        directory = pathlib.Path.cwd().resolve()

    files_getters = {
        f".{name}.toml": lambda dictionary: dictionary,
        "pyproject.toml": lambda dictionary: dictionary.get("tool", {}).get(
            name, {}
        ),
    }

    for file, getter in files_getters.items():
        path = _load.project_root(file, vcs, start=directory)
        if path is not None:
            with path.open("rb") as handle:
                return getter(tomllib.load(handle))

    return {}
