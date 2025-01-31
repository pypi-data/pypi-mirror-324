# SPDX-FileCopyrightText: © 2024 nosludge <https://github.com/nosludge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Extensions for `commition`.

Extensions make it possible to use `commition` with other tools,
frameworks, or libraries. Sometimes they are an entrypoints
used by another program to get the version of the project.

Warning:
    To use the extensions, you need to install the corresponding packages
    or use an optional dependency defined by each extension (see their
    documentation for more information).

Warning:
    The extensions __will not__ be available without specific
    options, importing them directly will raise an ImportError.

"""

from __future__ import annotations

from . import _installed

__all__ = []

if _installed.GIT:
    from ._git import git

    __all__ += ["git"]
else:  # pragma: no cover
    pass

if _installed.TOOLOAD:
    from . import pdm

    __all__ += ["pdm"]
else:  # pragma: no cover
    pass
