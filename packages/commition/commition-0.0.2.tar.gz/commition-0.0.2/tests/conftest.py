# SPDX-FileCopyrightText: © 2024 nosludge <https://github.com/nosludge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Shared tests functionality.

Each shared functionality should be placed in this file and
added to the `pytest` namespace (later reused by other tests).

"""

from __future__ import annotations

import dataclasses
import typing

import pytest


@dataclasses.dataclass
class CommitionVersionTester:
    """Stripped-down version tester for `commition`.

    Attributes:
        major:
            Major version number.
        minor:
            Minor version number.
        patch:
            Patch version

    """

    major: int = 0
    minor: int = 0
    patch: int = 0

    def __str__(self) -> str:
        """Return version as string."""
        return f"{self.major}.{self.minor}.{self.patch}"

    def to_tuple(self) -> tuple[int, int, int]:
        """Return version as tuple."""
        return self.major, self.minor, self.patch

    def bump(
        self, commit_type: typing.Literal["fix", "feat", "feat!", "fix!"]
    ) -> None:
        """Bump version based on commit type.

        Args:
            commit_type:
                Commit type to bump version for.

        """
        if commit_type in {"fix!", "feat!"}:
            self.major += 1
            self.minor, self.patch = 0, 0
        elif commit_type == "feat":
            self.minor += 1
            self.patch = 0
        elif commit_type == "fix":
            self.patch += 1


pytest.CommitionVersionTester = CommitionVersionTester
"""Hack making `CommitionVersionTester` globally test available."""
