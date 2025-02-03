"""An augmented ArgumentParser subclass."""

from argparse import ArgumentParser, Namespace
from collections.abc import Sequence
from gettext import gettext as _
from typing import Any, overload, TypeVar
from .base import override


_N = TypeVar('_N')


class ModifiedArgumentParser(ArgumentParser):
    """An enhanced argument parser subclass."""

    @overload
    def parse_known_args(self, args: Sequence[str] | None = None,
                         namespace: None = None) -> tuple[Namespace, list[str]]: ...

    @overload
    def parse_known_args(self, args: Sequence[str] | None,  # pylint: disable=signature-differs
                         namespace: _N) -> tuple[_N, list[str]]: ...

    @overload
    def parse_known_args(self, *, namespace: _N) -> tuple[_N, list[str]]:  ...  # pylint: disable=arguments-differ

    # FIXME determine whether signature can be simplified, possibly:
    # _N = TypeVar('_N', bound=Namespace)
    # def parse_known_args(self, args: Sequence[str] | None = None,
    #                      namespace: _N | None = None) -> tuple[_N, list[str]]:

    @override
    def parse_known_args(self, args: Sequence[str] | None = None,
                         namespace: Any = None) -> tuple[Any, list[str]]:
        """
        Force `parse_known_args` to behave like `parse_args`.
        This ensures that usage statements for unexpected arguments
        are as specific as possible for the chosen subcommand.
        Note that `add_subparsers` calls will reuse the caller's own
        class by default.

        :param args: the list of strings to parse
        :param namespace: an object to take the attributes, defaulting to
          an argparse.Namespace object
        :returns: a two item tuple containing the populated namespace and
          the list of remaining argument strings
        """
        args, argv = super().parse_known_args(args, namespace)
        if argv:
            msg = _('unrecognized arguments: %s')
            self.error(msg % ' '.join(argv))
        return args, argv
