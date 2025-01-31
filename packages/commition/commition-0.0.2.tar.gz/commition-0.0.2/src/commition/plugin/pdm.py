# SPDX-FileCopyrightText: © 2024 nosludge <https://github.com/nosludge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Extensions for [`pdm`](https://pdm-project.org/en/latest/) package manager.

Warning:
    To use the `pdm` module, you need to install the `pdm` option
    of the `commition` package.
"""

from __future__ import annotations

import tooload

from . import _installed

if _installed.GIT:
    import collections
    import typing

    from ._git import git as g

    if typing.TYPE_CHECKING:
        import re

        from git import Repo

    def git(  # noqa: PLR0913
        repository: Repo | None = None,
        path_include: collections.abc.Iterable[str | re.Pattern] | None = None,
        path_exclude: collections.abc.Iterable[str | re.Pattern] | None = None,
        author_name_include: collections.abc.Iterable[str | re.Pattern]
        | None = None,
        author_name_exclude: collections.abc.Iterable[str | re.Pattern]
        | None = None,
        author_email_include: collections.abc.Iterable[str | re.Pattern]
        | None = None,
        author_email_exclude: collections.abc.Iterable[str | re.Pattern]
        | None = None,
        major_regex: collections.abc.Iterable[str | re.Pattern] | None = None,
        minor_regex: collections.abc.Iterable[str | re.Pattern] | None = None,
        patch_regex: collections.abc.Iterable[str | re.Pattern] | None = None,
        unrecognized_messages: typing.Literal["ignore", "error"] | None = None,
    ) -> str:
        """Get the version of the to use with `pdm` package manager.

        Warning:
            To use this function, you need to install the `pdm` option
            or have [`tooload`](https://github.com/nosludge/tooload)
            and [`gitpython`](https://github.com/gitpython-developers/GitPython)
            packages installed.

        This function calculates the version as follows:

        - Uses `tooload.config` to get the configuration
        - Uses `commition.plugin.git` to obtain the version

        You can configure the `commition` plugin either by adding a
        `.commition.toml` file to the root of your project or by
        using the `[tool.commition]` section in your `pyproject.toml`.

        Warning:
            Configuration `keys` should be named as the arguments
            of this function.

        Note:
            Default values will be inferred from the config file, if provided,
            otherwise defaults from the `commition.plugin.git`
            will be used, refer to this function's signature and documentation
            for more information.

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
            major_regex:
                The regex for the major version. By default, it matches
                `feat!:` and `fix!:` messages OR `BREAKING CHANGE` anywhere
                in the message.
            minor_regex:
                The regex for the minor version. By default, it matches
                `feat:` messages.
            patch_regex:
                The regex for the patch version. By default, it matches
                `fix:` messages.
            unrecognized_messages:
                The behavior for unrecognized messages. It can be
                either "exclude" or "error".

        Returns:
            [`pdm`](https://pdm-project.org/en/latest/) compatible
            version of the project.
        """
        config = collections.defaultdict(
            lambda: None, tooload.config("commition")
        )

        return str(
            g(
                path_include=path_include or config["path_include"],
                path_exclude=path_exclude or config["path_exclude"],
                author_name_include=author_name_include
                or config["author_name_include"],
                author_name_exclude=author_name_exclude
                or config["author_name_exclude"],
                author_email_include=author_email_include
                or config["author_email_include"],
                author_email_exclude=author_email_exclude
                or config["author_email_exclude"],
                repository=repository or config["repository"],
                major_regex=major_regex or config["major_regex"],
                minor_regex=minor_regex or config["minor_regex"],
                patch_regex=patch_regex or config["patch_regex"],
                unrecognized_messages=unrecognized_messages
                or config["unrecognized_messages"],
            )
        )
else:  # pragma: no cover
    pass
