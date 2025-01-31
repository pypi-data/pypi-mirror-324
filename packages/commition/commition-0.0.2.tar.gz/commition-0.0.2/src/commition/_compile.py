# SPDX-FileCopyrightText: © 2025 nosludge <https://github.com/nosludge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Compile regexes."""

from __future__ import annotations

import re


def multiple(
    regexes: list[re.Pattern] | list[str] | None,
) -> re.Pattern | None:
    """Compile the regex if it is a string.

    Args:
        regexes:
            The regex to compile. If it is a string, it will be compiled.

    Returns:
        The compiled regex or None.

    """
    return (
        re.compile("(" + "|".join(f"({r})" for r in regexes) + ")")
        if regexes
        else None
    )
