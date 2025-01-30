"""Constant values of the project."""

from __future__ import annotations

import platform
import typing

if typing.TYPE_CHECKING:
    from typing import Final

#: Name of the running operating system.
OS_NAME: Final[str] = platform.system()

#: OS name of Windows.
OS_NAME_WINDOWS: Final[str] = "Windows"
