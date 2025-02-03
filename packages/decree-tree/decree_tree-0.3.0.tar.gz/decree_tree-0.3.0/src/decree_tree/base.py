"""Define some basic constants and classes for general use."""

from argparse import (
    ArgumentParser,
    _SubParsersAction,  # pylint: disable=protected-access
)
import sys
from typing import Any, Protocol, TypeAlias, TYPE_CHECKING

# Handle Python version compatibility
# if sys.version_info >= (3, 11):
#     from typing import Self
# else:
#     from typing_extensions import Self
if sys.version_info >= (3, 12):
    from typing import override  # pylint: disable=unused-import
else:
    from typing_extensions import override


# Define custom exceptions
class InvalidName(IndexError):
    """
    A custom exception indicating that a DecreeTree with
    a particular name cannot be found.
    """


# Handle class that is generic in stubs but not in runtime
if TYPE_CHECKING:
    SubParsersType = _SubParsersAction[ArgumentParser]
else:
    SubParsersType = _SubParsersAction


class SupportsLT(Protocol):  # pylint: disable=too-few-public-methods
    """A typing protocol for supporting the ``__lt__`` method."""

    def __lt__(self, __other: Any) -> bool: ...


class SupportsGT(Protocol):  # pylint: disable=too-few-public-methods
    """A typing protocol for supporting the ``__gt__`` method."""

    def __gt__(self, __other: Any) -> bool: ...


# Support typing for sort()
SupportsComparison: TypeAlias = SupportsLT | SupportsGT
