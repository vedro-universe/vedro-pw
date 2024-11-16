"""
Provides compatibility for the `Unpack` type hint across Python versions.

This module ensures that the `Unpack` type hint is available regardless of whether it is natively
available in the `typing` module (for newer Python versions) or needs to be imported from
`typing_extensions`. If neither is available, it defines a fallback for `Unpack`.
"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Unpack
else:
    try:
        from typing import Unpack
    except ImportError:
        try:
            from typing_extensions import Unpack
        except ImportError:
            from typing import Any, TypeVar, Union
            _T = TypeVar("_T")
            Unpack = Union[_T, Any]


__all__ = ("Unpack",)
