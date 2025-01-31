# SPDX-FileCopyrightText: © 2024 nosludge <https://github.com/nosludge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Core functionality of `commition`."""

from __future__ import annotations

import re
import typing

from . import _compile, error

if typing.TYPE_CHECKING:
    import collections


class Version:
    """Conventional commits based versioning.

    You can use this class to calculate the next version based on the
    conventional commits messages.

    Attributes:
        major: The major version.
        minor: The minor version.
        patch: The patch version.
    """

    @classmethod
    def from_string(
        cls,
        version: str,
        **kwargs: typing.Any,
    ) -> Version:
        """Create a new version from a string.

        Args:
            version:
                The version as a string.
            **kwargs:
                Keyword arguments to pass to the `Version` constructor.

        Returns:
            The new version.
        """
        major, minor, patch = version.split(".")
        return Version.from_numbers(
            int(major), int(minor), int(patch), **kwargs
        )

    @classmethod
    def from_numbers(
        cls,
        major: int,
        minor: int,
        patch: int,
        **kwargs: typing.Any,
    ) -> Version:
        """Create a new version from numbers.

        Args:
            major:
                The major version.
            minor:
                The minor version.
            patch:
                The patch version.
            **kwargs:
                Keyword arguments to pass to the `Version` constructor.

        Returns:
            The new version.
        """
        version = Version(**kwargs)
        version.major = major
        version.minor = minor
        version.patch = patch
        return version

    @classmethod
    def from_messages(
        cls,
        messages: collections.abc.Iterable[str],
        **kwargs: typing.Any,
    ) -> Version:
        """Create a new version from an iterable of messages.

        Args:
            messages:
                An iterable of messages.
            **kwargs:
                Keyword arguments to pass to the `Version` constructor.
        """
        version = Version(**kwargs)

        for message in messages:
            version.bump_from_message(message)

        return version

    def __init__(
        self,
        major_regex: collections.abc.Iterable[str | re.Pattern] | None = None,
        minor_regex: collections.abc.Iterable[str | re.Pattern] | None = None,
        patch_regex: collections.abc.Iterable[str | re.Pattern] | None = None,
        unrecognized_messages: typing.Literal["ignore", "error"] | None = None,
    ) -> None:
        """Initialize the version.

        Warning:
            You likely want to use one of `from_*` methods to create a new
            instance instead.

        Note:
            By default, all versions will be set to `0`, so the full
            version is `0.0.0`.

        Args:
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
                either "ignore" or "error".
        """
        self.major_regex = (
            re.compile(r".*BREAKING CHANGE.*|^(feat|fix)(\(.*?\))?!: .*")
            if major_regex is None
            else _compile.multiple(major_regex)
        )
        self.minor_regex = (
            re.compile("^feat(\\(.*?\\))?: .*")
            if minor_regex is None
            else _compile.multiple(minor_regex)
        )
        self.patch_regex = (
            re.compile("^fix(\\(.*?\\))?: .*")
            if patch_regex is None
            else _compile.multiple(patch_regex)
        )

        if unrecognized_messages is None:
            unrecognized_messages = "ignore"

        self.unrecognized_messages = unrecognized_messages

        self.patch: int = 0
        self.minor: int = 0
        self.major: int = 0

    def regexes(self) -> dict[str, re.Pattern]:
        """Yield the regexes for the version types.

        Each regex has a key identifying the version type.

        Yields:
            The version type and the regex.
        """
        yield "major", self.major_regex
        yield "minor", self.minor_regex
        yield "patch", self.patch_regex

    def bump_from_message(self, message: str) -> Version:
        """Bump the version based on a message.

        Args:
            message: The message to bump the version from.

        Raises:
            MessageUnrecognizedError: If the message is not recognized
                by any of the regexes and `unrecognized_messages`
                is set to "error".

        Returns:
            The current instance of the class.
        """
        for version, regex in self.regexes():
            if regex.match(message):
                getattr(self, f"bump_{version}")()
                return self

        if self.unrecognized_messages == "error":
            raise error.MessageUnrecognizedError(message)

        return self

    def bump_major(self) -> None:
        """Bump the major version.

        Warning:
            This method mutates the instance.

        """
        self.major += 1
        self.minor = 0
        self.patch = 0

    def bump_minor(self) -> None:
        """Bump the minor version.

        Warning:
            This method mutates the instance.

        """
        self.minor += 1
        self.patch = 0

    def bump_patch(self) -> None:
        """Bump the patch version.

        Warning:
            This method mutates the instance.

        """
        self.patch += 1

    def __str__(self) -> str:
        """Return the version as a string."""
        return f"{self.major}.{self.minor}.{self.patch}"

    def __eq__(self, other: object) -> bool:
        """Check if two versions are equal.

        Args:
            other:
                Object to compare against. Should be
                an instance of `Version`

        """
        return (
            self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch
        )
