"""Determine the version of the package."""

from importlib.metadata import version

_PACKAGE_NAME = "decree-tree"  # use the "PyPI" name, not the "import" name
__version__ = version(_PACKAGE_NAME)
