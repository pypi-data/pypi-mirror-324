# SPDX-FileCopyrightText: © 2025 nosludge <https://github.com/nosludge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Regex matching functions."""

from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import re

    import git as g


def item(
    what: str, include: re.Pattern | None, exclude: re.Pattern | None
) -> bool:
    """Check if the `what` is included based on the `include` and `exclude`.

    Note:
        Empty `include` are treated as include-everything.
        Empty `exclude` are treated as include-everything as well.

    Note:
        exclude regexes take precedence over include regexes.

    Args:
        what:
            The string to check.
        include:
            The regex to include the string.
        exclude:
            The regex to exclude.

    Returns:
        True if the `what` is included, False otherwise.

    """
    return (include is None or include.search(what)) and (
        exclude is None or not exclude.search(what)
    )


def path(
    commit: g.Commit, include: re.Pattern | None, exclude: re.Pattern | None
) -> bool:
    """Check if the commit touched the file based regexes.

    Note:
        Empty `include` are treated as include-everything.
        Empty `exclude` are treated as include-everything as well.

    Note:
        exclude regexes take precedence over include regexes.

    Args:
        commit:
            The commit to check.
        include:
            The regex to include the file.
        exclude:
            The regex to exclude the file.

    Returns:
        True if the commit touched the file, False otherwise.
    """
    if include is None and exclude is None:
        return True

    return not commit.diff() or any(
        item(diff.a_path, include, exclude) for diff in commit.diff()
    )
