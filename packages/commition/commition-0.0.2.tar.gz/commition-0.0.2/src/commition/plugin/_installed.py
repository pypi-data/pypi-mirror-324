# SPDX-FileCopyrightText: © 2024 nosludge <https://github.com/nosludge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Module defining which extras are installed."""

from __future__ import annotations

import importlib.util


def _modules_exist(*names: str) -> bool:
    """Check if module(s) are installed.

    Used for conditional imports throughout the project and
    conditional definitions of functionalities.

    Args:
        *names: Module names to check.

    Returns:
        True if all modules are installed, False otherwise.
    """
    return all(importlib.util.find_spec(name) is not None for name in names)


GIT = _modules_exist("git")
"""True if the git module is installed, False otherwise."""

TOOLOAD = _modules_exist("tooload")
"""True if the pdm module is installed, False otherwise."""
