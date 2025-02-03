"""The multi-level command."""

import argparse
import sys
from typing import (
    Any, Callable, cast, ClassVar, Sequence, Type, TypeAlias, Union
)
from .base import override, SubParsersType, SupportsComparison
from .decree import Decree
from .tree import Tree


# Cannot use Decree for parents or children as they lack proper handling
# FIXME use `type` in newer Python versions, and also replace Union
DecreeTreeType: TypeAlias = 'DecreeTree'


# pylint: disable=too-many-public-methods
class DecreeTree(Tree[DecreeTreeType], Decree):
    """A class for creating a command-line program using ``argparse`` subcommands."""

    # Make DecreeTree itself abstract
    name = ''
    help = ''

    #: the name of the pseudo-option used to identify the active command, allowing override
    exec_obj_opt: ClassVar[str] = '_exec_obj_'

    @override
    def __init__(self, *,  # pylint: disable=useless-parent-delegation
                 name: str | None = None,
                 inherit: bool = True,
                 prog_is_name: bool = False,
                 version: str | None = None,
                 ) -> None:
        """
        Initialize the variables specific to the combined DecreeTree.
        This method exists to make its interface explicit, rather than
        relying on unspecified ``**kwargs``.

        :param name: the command name, if overriding it for the instance
        :param inherit: whether parents are considered when invoking a DecreeTree
        :param prog_is_name: whether to use ``self.name`` as the program name in help
        :param version: version information; use ``--version`` to show
        """
        super().__init__(name=name, prog_is_name=prog_is_name, version=version)

        #: whether parents are considered when invoking a DecreeTree
        self.inherit = inherit

    @override
    def repr_kwargs(self) -> dict[str, str | bool | None]:
        """
        Provide relevant non-default __init__ kwargs for __repr__.

        :raises KeyError: if unexpected keys are present in super call
        :returns: the relevant kwargs in the desired order
        """
        super_kwargs = super().repr_kwargs()
        if self.inherit is not True:
            super_kwargs['inherit'] = self.inherit
        ordered_keys = ['name', 'inherit', 'prog_is_name', 'version']
        if not set(super_kwargs.keys()).issubset(ordered_keys):
            raise KeyError(f"Unexpected repr_kwargs keys in: {super_kwargs.keys()}")
        kwargs = {k: super_kwargs[k] for k in ordered_keys if k in super_kwargs}
        return kwargs

    # Intentionally not overriding default DecreeTree.__str__() (from Tree) here

    @override
    @property
    def get_name(self) -> str:
        """
        Provides the name of the instance, to facilitate separation of
        concerns via the use of Tree.

        :returns: the name of the instance
        """
        return self.name

    @property
    def structure(self) -> str:
        """
        Show the structure of the nested tree.
        Relies on str() including a list of parents.

        :returns: the structure string
        """
        class_path = self.__class__.__module__ + '.' + self.__class__.__qualname__
        structure = str(self) + f': {class_path}'
        for child in self.children:
            structure += '\n' + child.structure
        return structure

    @override
    def run(
        self,
        argv: Sequence[str] | None = None,
        options: argparse.Namespace | None = None,
        *,
        debug_tracing: bool = False,
        argument_parser_class: type[argparse.ArgumentParser] | None = None,
    ) -> Any:
        """
        Run the command via command line or with defined arguments.
        The command object executing ``run()`` will be considered the
        to be the root of the command, aside from any inherited
        processing. To override the actual command line arguments,
        pass to ``argv`` either a space-delimited string
        of tokens or a sequence of individual token strings.

        :param argv: command-line arguments to parse
        :param options: processed arguments, circumventing parse_args if specified
        :param debug_tracing: whether to show debug tracing statements
        :param argument_parser_class: an override for the argument parser class
        :raises Exception: if any are raised within the running DecreeTree
        :returns: the results from execution, if any
        """
        self.set_debug_tracing(debug_tracing)
        self.debug_print("Running '{self}'")
        try:
            if argument_parser_class is not None:
                self.argument_parser_class = argument_parser_class
            if not hasattr(self, 'parser'):
                self.configure_parser_tree()
            self.preprocess_options(argv, options)
            exec_obj: DecreeTreeType = getattr(self.options, self.exec_obj_opt)
            exec_obj.set_options(self.options)
            # exec_obj.set_options(exec_obj._decree_parser.parse_args(argv))
            # FIXME use line above if we make a top-level parser for each DecreeTree?
            exec_obj.process_options()
            results = exec_obj.execute()
        except Exception as exc:
            self.handle_run_exception(exc)
            raise
        return results

    def configure_parser(self, subparsers: SubParsersType | None = None) -> None:
        """
        Configure the parser for this object. Typically not called by
        nor overridden in end-user code.

        :param subparsers: the subparsers object from a parent, if any
        :raises ValueError: when the configuration of the name or prog is incorrect
        """
        if subparsers:  # self is a subcommand
            self.debug_print("Configuring subcommand parser for '{self}'")
            if not self.name:
                raise ValueError("Expected non-empty name")
            subparser_options: dict[str, Any] = {
                'help': self.help,
                'description': self.__doc__,
                'allow_abbrev': False,
            }
            subparser_options |= self.parser_options(True)
            self._decree_parser = subparsers.add_parser(self.name, **subparser_options)
        else:  # self is the root command, no ``help`` argument
            super().configure_parser()

    def configure_parser_tree(self,
                              subparsers: SubParsersType | None = None,
                              parser: argparse.ArgumentParser | None = None) -> None:
        """
        Configure the parser for this tree. Typically not called by
        nor overridden in end-user code.

        :param subparsers: the subparsers object from a parent, if any
        :param parser: the parser to which arguments will be added, if not ``self._decree_parser``
        """
        self.debug_print("Configuring parser tree for '{self}'{tree}{parser}",
                         tree=' associated with parent subparsers object' if subparsers else '',
                         parser=' with parser' if parser else '')
        self.configure_parser(subparsers)
        active_parser = parser or self._decree_parser
        active_parser.set_defaults(**{self.exec_obj_opt: self})
        if self.children:
            subparsers_options: dict[str, Any] = {
                'description': None,
                'required': True,
                # 'parser_class': self.argument_parser_class,  # unset: using value from tree root
                # 'help': "select a subcommand",
                # 'metavar': "SUBCOMMAND",
            }
            subparsers_options |= self.subparsers_options()
            child_subparsers = active_parser.add_subparsers(**subparsers_options)
            for child in self.children:
                child.configure_parser_tree(child_subparsers)  # pylint: disable=protected-access
        else:
            # Arguments added at this level will not be usable at this level if
            # there are also subcommands. If this were to change, it would likely
            # involve an instance/class variable, changes here, and possibly
            # changing ``required`` to ``False`` in ``subparsers_options()``.
            self.add_arguments(active_parser)

    def subparsers_options(self) -> dict[str, Any]:
        """
        Add to and override options passed to ``add_subparsers``.

        :returns: the options to provide to the subparsers object creator
        """
        return {}

    def handle_run_exception(self, exc: Exception) -> None:
        """
        Handle general exceptions raised within the ``run`` method.

        :param exc: the exception that was raised
        """
        note = f"Failed in {self.__class__.__qualname__} '{self}'"
        if sys.version_info >= (3, 11):
            exc.add_note(note)  # pylint: disable=no-member
        else:
            print(note)

    def set_debug_tracing(self, debug_tracing: bool) -> None:
        """
        Set self.debug_tracing for this DecreeTree and all of its
        children, recursively.

        :param debug_tracing: whether debug trace output should be enabled
        """
        self.debug_tracing = debug_tracing
        # Do not expect to need to call self.parent.set_debug_tracing
        for child in self.children:
            child.set_debug_tracing(debug_tracing)

    def set_options(self, options: argparse.Namespace) -> None:
        """
        Set self.options for the DecreeTree. This is typically called by the
        top-level run command on the exec_obj command to set options for all
        ``DecreeTree`` objects in the chain of the executed subcommand.
        It is normally not overridden by subclasses of ``DecreeTree``.

        :param options: the parsed but unprocessed options to propagate
        """
        if self.parent:
            # Not checking self.inherit, since this should always occur
            self.parent.set_options(options)
        for key, value in vars(options).items():
            # Keep self.options as the same object
            setattr(self.options, key, value)
        self.debug_print("Setting options for '{self}'")

    @override
    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """
        Add arguments to ``parser`` (not ``self._decree_parser``), if any, optionally
        adding arguments "inherited" from the parent ``DecreeTree``.
        Subclass overrides typically include a call to ``super().add_arguments(parser)``.
        Handle manual argument processing in ``process_options``, not here.

        :param parser: the parser to which arguments will be added
        """
        if self.inherit and self.parent:
            self.parent.add_arguments(parser)
        super().add_arguments(parser)  # FIXME not sure how to bring in --version

    @override
    def process_options(self) -> None:
        """
        Perform any needed processing on the options, prior to execution,
        optionally processing arguments "inherited" from the parent ``DecreeTree``.
        Options for all subcommands in the executed chain are available here.
        Subclass overrides typically include a call to ``super().process_options()``.
        """
        if self.inherit and self.parent:
            self.parent.process_options()
        super().process_options()  # just for debug_print

    @override
    def execute(self) -> Any:
        """
        Execute [sub]command processing, optionally executing processing
        "inherited" from the parent ``DecreeTree``.
        Options for all subcommands in the executed chain are available here.
        Subclass overrides typically include a call to ``super().execute()``.

        :returns: any required data
        """
        results = None
        if self.inherit and self.parent:
            results = self.parent.execute()
        super().execute()  # just for debug_print, ignore None return value
        return results

    # The next set of methods are short names for commonly-used Tree methods.

    def add(self, child: DecreeTreeType | Type[DecreeTreeType]) -> DecreeTreeType:
        """
        A shortcut to append a new child, equivalent to ``append_child``.

        :param child: the DecreeTree object, class, or subclass to append
        :returns: the child itself, in case it was created within this method
        """
        return self.append_child(child)

    def get(self, *args: str) -> DecreeTreeType:
        r"""
        Look up and provide the nested child object, equivalent to ``get_child``.
        This can indirectly raise InvalidName if a matching object cannot be found.

        :param \*args: the nested path of names to the requested object
        :returns: the object found
        """
        return self.get_child(*args)

    # The methods below override the generic type signatures of Tree, only to
    # make them cleaner for IDE type hints, Sphinx documentation, etc.
    # It would be great if this was not necessary.
    # Note that docstrings are intentionally not recreated here, as the
    # docstrings from Tree appear to still picked up by IDEs, linters, static
    # type checkers, and documentation generators.
    # FIXME re-add docstrings to change Tree to DecreeTree

    @override
    def append_child(self, child: DecreeTreeType | Type[DecreeTreeType]) -> DecreeTreeType:
        return super().append_child(child)

    @override
    @property
    def children(self) -> list[DecreeTreeType]:
        return super().children

    @override
    def find_child(self, name: str, raise_exception: bool = False) -> Union[DecreeTreeType, None]:
        return super().find_child(name, raise_exception)

    # This override constrains the type of the returned object,
    # via ``cast``, due to the original 'Tree[T]' return type.
    @override
    def get_child(self, *args: str) -> DecreeTreeType:
        return cast(DecreeTreeType, super().get_child(*args))

    @override
    def insert_child(self,
                     index: int,
                     child: DecreeTreeType | Type[DecreeTreeType],
                     ) -> DecreeTreeType:
        return super().insert_child(index, child)

    @override
    @property
    def parent(self) -> Union[DecreeTreeType, None]:
        return super().parent

    @override
    @property
    def parents(self) -> list[DecreeTreeType]:
        return super().parents

    @override
    def replace_child(self,
                      name: str,
                      child: Union[DecreeTreeType, Type[DecreeTreeType]],
                      raise_exception: bool = False,
                      ) -> Union[DecreeTreeType, None]:
        return super().replace_child(name, child, raise_exception)

    @override
    def sort_children(self, *,
                      key: Callable[[DecreeTreeType], SupportsComparison] | None = None,
                      reverse: bool = False) -> None:
        super().sort_children(key=key, reverse=reverse)
