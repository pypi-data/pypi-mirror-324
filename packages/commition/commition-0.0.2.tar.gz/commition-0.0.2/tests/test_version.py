# SPDX-FileCopyrightText: © 2024 nosludge <https://github.com/nosludge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Test `commition.Version` class."""

from __future__ import annotations

import hypothesis
import pytest

import commition


def create_version(commit_types: list[str]) -> commition.Version:
    """Create version based on commit types.

    Args:
        commit_types:
            List of commit types. Contain only `fix` and `feat` types
            with optional `!` at the end.

    Returns:
        Version based on commit types.

    """
    version = pytest.CommitionVersionTester()
    for commit_type in commit_types:
        version.bump(commit_type)

    return commition.Version.from_numbers(*version.to_tuple())


@pytest.mark.parametrize("major_regex", (None, (".*", "bbb")))
@pytest.mark.parametrize("minor_regex", (None, (".*", "ccc")))
@pytest.mark.parametrize("patch_regex", (None, (".*", "ddd")))
@hypothesis.given(
    commit_types=hypothesis.strategies.lists(
        hypothesis.strategies.sampled_from(["fix", "feat", "feat!", "fix!"])
    )
)
def test_version_from_messages(
    commit_types: list[str],
    major_regex: tuple[str] | None,
    minor_regex: tuple[str] | None,
    patch_regex: tuple[str] | None,
) -> None:
    """Test `commition.Version.from_messages` method.

    This test focuses on `regex` arguments and order of commit evaluation
    (from `major`, through `minor` to `patch`).

    Args:
        commit_types:
            List of commit types. Contain only `fix` and `feat` types
            with optional `!` at the end.
        major_regex:
            Regular expression for major version.
        minor_regex:
            Regular expression for minor version.
        patch_regex:
            Regular expression for patch version.
    """
    messages = [f"{commit_type}: bla bla bla" for commit_type in commit_types]
    test_version = create_version(commit_types)

    commition_version = commition.Version.from_messages(
        messages,
        major_regex=major_regex,
        minor_regex=minor_regex,
        patch_regex=patch_regex,
    )

    # ".*" swallows all commits, all should be major versions
    if major_regex:
        assert commition_version.major == len(messages)
    # We can only assert something about major if minor swallows all
    elif major_regex is None and minor_regex:
        assert commition_version.major == test_version.major
    # If none are specified, it should be a standard version
    else:
        assert (
            commition.Version.from_string(str(test_version))
            == commition_version
        )


def test_unrecognized_commit_type() -> None:
    """Test `commition.Version.bump` method with unrecognized commit type."""
    version = commition.Version(unrecognized_messages="error")
    with pytest.raises(commition.error.MessageUnrecognizedError):
        version.bump_from_message("unknown")
