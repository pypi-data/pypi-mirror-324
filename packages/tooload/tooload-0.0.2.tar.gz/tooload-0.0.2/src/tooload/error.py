# SPDX-FileCopyrightText: © 2024 nosludge <https://github.com/nosludge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Custom exceptions of the `tooload` package."""

from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import pathlib


class TooloadError(Exception):
    """Base class for exceptions in this module."""


class ConfigMissingError(TooloadError):
    """Exception raised when the configuration file is missing."""

    def __init__(self, config: pathlib.Path) -> None:
        """Initialize the exception with the missing configuration file path.

        Args:
            config: The path to the missing configuration file.
        """
        super().__init__(f"Specified configuration file {config} not found.")
