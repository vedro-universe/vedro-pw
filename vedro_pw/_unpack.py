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
