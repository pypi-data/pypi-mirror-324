"""
The decree-tree package provides a lightweight means
for defining nested command-line interfaces.
"""

from ._version import __version__
from .assembled import DecreeTree
from .base import InvalidName

__all__ = [
    '__version__',
    'DecreeTree',
    'InvalidName',
]
