# SPDX-FileCopyrightText: © 2024 nosludge <https://github.com/nosludge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""tooload official documentation.

Minimalistic library for loading tool-specific configuration from
configuration files (either `.tool.toml` or `pyproject.toml`).

"""

from __future__ import annotations

from importlib.metadata import version

from . import error
from ._config import config

__version__ = version("tooload")
"""Current tooload version."""

del version

__all__: list[str] = [
    "__version__",
    "config",
    "error",
]
