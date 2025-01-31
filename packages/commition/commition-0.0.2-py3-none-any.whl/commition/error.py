# SPDX-FileCopyrightText: © 2024 nosludge <https://github.com/nosludge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Custom exceptions of `commition`."""

from __future__ import annotations


class CommitionError(Exception):
    """Base class for all exceptions raised by `commition`."""


class MessageUnrecognizedError(CommitionError):
    """Raised when the message is not recognized by any regexes."""

    def __init__(self, message: str) -> None:
        """Initialize the error.

        Args:
            message:
                The message which was not recognized by any regexes.

        """
        self.message = message

        super().__init__(
            f"Message '{message}' is not recognized by any of the provided regexes."
        )
