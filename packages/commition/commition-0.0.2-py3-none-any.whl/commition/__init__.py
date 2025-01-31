# SPDX-FileCopyrightText: © 2024 nosludge <https://github.com/nosludge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""commition official documentation."""

from __future__ import annotations

from importlib.metadata import version

from . import error, plugin
from ._version import Version

__version__ = version("commition")
"""Current commition version."""

del version

__all__: list[str] = [
    "Version",
    "__version__",
    "error",
    "plugin",
]
