"""Module containing type annotation specific utilities."""

from __future__ import annotations

import inspect
import types
import typing

if typing.TYPE_CHECKING:
    from collections.abc import Callable


def find_parameter_by_type_annotation(
    function: Callable[..., typing.Any],
    target_type: type | types.UnionType | None,
) -> inspect.Parameter | None:
    """Find first occurrence of a parameter in a callable by type annotation.

    Parameters
    ----------
    function
        Callable to inspect.
    target_type
        Type annotation to look for.

    Returns
    -------
    inspect.Parameter
        First parameter that matches the type annotation.
    None
        If no matching parameter is found.
    """
    signature = inspect.signature(function, eval_str=True)

    if target_type is None:
        target_types = (type(target_type),)
    else:
        target_types = (
            typing.get_args(target_type)
            if isinstance(target_type, types.UnionType)
            else (target_type,)
        )

    for p in signature.parameters.values():
        if p.annotation is None:
            p_types = (type(p.annotation),)
        else:
            p_types = (
                typing.get_args(p.annotation)
                if isinstance(p.annotation, types.UnionType)
                else (p.annotation,)
            )

        if any(issubclass(t, target_types) for t in p_types):
            return p

    return None
