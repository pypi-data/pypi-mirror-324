# SPDX-FileCopyrightText: © 2024 nosludge <https://github.com/nosludge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""`cogeol` lets you to obtain the supported Python versions.

This module provides a function to get the latest Python versions from the
endoflife.date API. The function caches the result for 24 hours (by default)
to avoid making too many requests to the API and to speed up the results.

This module will likely be used with `cog` to automate the generation
of supported Python versions in the project (e.g. in `pyproject.toml`
or source code).

- See https://endoflife.date/python for more information about the API.
- See https://github.com/nedbat/cog for more information about the cog tool.

See [python-template](https://github.com/nosludge/python-template/blob/main/pyproject.toml#L)
for an example of how to use this module with cog.

"""

from __future__ import annotations

from importlib.metadata import version

from . import error
from ._versions import scientific, versions

__version__ = version("cogeol")
"""Current cogeol version."""

del version

__all__: list[str] = [
    "__version__",
    "error",
    "scientific",
    "versions",
]
