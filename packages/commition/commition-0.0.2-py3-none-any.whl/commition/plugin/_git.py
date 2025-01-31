# SPDX-FileCopyrightText: © 2024 nosludge <https://github.com/nosludge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Extensions using `gitpython` package."""

from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import re

import git as g

from .. import _compile
from .._version import Version
from . import _match


def git(  # noqa: PLR0913
    repository: g.Repo | None = None,
    path_include: list[re.Pattern] | list[str] | None = None,
    path_exclude: list[re.Pattern] | list[str] | None = None,
    author_name_include: list[re.Pattern] | list[str] | None = None,
    author_name_exclude: list[re.Pattern] | list[str] | None = None,
    author_email_include: list[re.Pattern] | list[str] | None = None,
    author_email_exclude: list[re.Pattern] | list[str] | None = None,
    **kwargs: typing.Any,
) -> Version:
    """Create a new version from the `git` repository.

    Commit messages are used to calculate the next version based on the
    regexes as defined in the `Version` constructor.

    Note:
        Same matching rules apply as in the `Version` constructor.

    Warning:
        `*_exclude` regexes take precedence over `*_include` regexes,
        the `*_include` regexes are checked first, then the `*_exclude` regexes
        might disinclude the `*_include` match

    Args:
        repository:
            The `git` repository. If not provided, will be
            searched in the parent directories.
        path_include:
            The regexes to include the path.
        path_exclude:
            The regexes to exclude the path.
        author_name_include:
            The regexes to include the author name.
        author_name_exclude:
            The regexes to exclude the author name.
        author_email_include:
            The regexes to include the author email.
        author_email_exclude:
            The regexes to exclude the author email.
        **kwargs:
            Keyword arguments to pass to the `Version` constructor.

    """
    if repository is None:
        repository = g.Repo(search_parent_directories=True)

    commits = (
        commit.message
        for commit in repository.iter_commits(reverse=True)
        if _match.item(
            commit.author.name,
            _compile.multiple(author_name_include),
            _compile.multiple(author_name_exclude),
        )
        and _match.item(
            commit.author.email,
            _compile.multiple(author_email_include),
            _compile.multiple(author_email_exclude),
        )
        and _match.path(
            commit,
            _compile.multiple(path_include),
            _compile.multiple(path_exclude),
        )
    )

    return Version.from_messages(
        commits,
        **kwargs,
    )
