# SPDX-FileCopyrightText: © 2024 nosludge <https://github.com/nosludge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""`cogeol` exceptions."""

from __future__ import annotations


class CogeolError(Exception):
    """Base exception for cogeol."""


class CacheDurationNegativeError(CogeolError):
    """Raised when the cache duration is negative."""

    def __init__(self, cache_duration: int) -> None:
        """Initialize the exception.

        Args:
            cache_duration:
                The cache duration that was negative.

        """
        super().__init__(
            "cache_duration must be `None` or a positive integer, "
            f" got '{cache_duration}'"
        )
