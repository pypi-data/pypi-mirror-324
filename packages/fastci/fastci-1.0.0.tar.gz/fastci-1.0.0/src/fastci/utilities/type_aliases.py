"""Module with type aliases for improved type safety and code clarity."""

from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from fastci.utilities.type_definitions import Packet

    Routable = Callable[..., Awaitable[Packet | None]]
