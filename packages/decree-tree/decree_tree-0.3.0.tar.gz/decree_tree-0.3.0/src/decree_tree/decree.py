"""The basic single-level command."""

import argparse
from typing import Any, ClassVar, Sequence
from .parser import ModifiedArgumentParser


class Decree:
    """A class for creating a command using ``argparse``."""

    #: short help text to use (allows __doc__ to be lengthy)
    help: ClassVar[str] = ''

    #: the name of the command, if not snake-cased class name
    name: str = ''

    #: the argument parser to use at the root level (and inherited there from)
    argument_parser_class: type[argparse.ArgumentParser] = ModifiedArgumentParser

    def __init__(self, *,
                 name: str | None = None,
                 prog_is_name: bool = False,
                 version: str | None = None) -> None:
        """
        Configure variables that change during execution.

        :param name: the command name, if overriding it for the instance
        :param prog_is_name: whether to use ``self.name`` as the program name in help
        :param version: version information to display
        :raises ValueError: if name is an empty string
        """
        super().__init__()

        #: the set of argparse-processed options to be used
        self.options: argparse.Namespace = argparse.Namespace()

        #: override the name for the instance
        if name == '':
            raise ValueError("Expected non-empty name argument, if any")
        if name is not None:
            self.name: str = name

        #: whether to use the ``name`` as the ``prog``, for help
        self.prog_is_name: bool = prog_is_name

        #: version information; use ``--version`` to show
        self.version: str | None = version

        #: the parser for this object
        self._decree_parser: argparse.ArgumentParser
        # Not initializing this to None in __init__ to avoid having to check for None
        # to satisfy typing, and using a dummy ArgumentParser seems unnecessary.

        #: whether to show debug tracing statements
        self.debug_tracing: bool = False

    def __init_subclass__(cls, **kwargs: Any) -> None:
        r"""
        Configure/override special class variables.

        :param \**kwargs: any keyword arguments needed for subclass customization
        """
        super().__init_subclass__(**kwargs)
        snake_cased_class_name = ''.join(
            '_' + c.lower() if c.isupper() else c for c in cls.__name__  # not __qualname__
        ).lstrip('_')
        cls.name = vars(cls).get(
            'name', getattr(cls, 'name', snake_cased_class_name) or snake_cased_class_name
        )
        cls.help = vars(cls).get(
            'help', cls.__doc__ or getattr(cls, 'help', '')
        )  # intentionally defaulting to '' rather than None

    def __repr__(self) -> str:
        class_path = f'{self.__class__.__module__}.{self.__class__.__qualname__}'
        kwargs = self.repr_kwargs()
        kwarg_list = ', '.join(f'{k}={v!r}' for k, v in kwargs.items())
        return f"{class_path}({kwarg_list})"

    def repr_kwargs(self) -> dict[str, str | bool | None]:
        """
        Provide relevant non-default __init__ kwargs for __repr__.

        :returns: the relevant kwargs in the desired order
        """
        kwargs: dict[str, str | bool | None] = {}
        if self.name != self.__class__.name:
            kwargs['name'] = self.name
        if self.prog_is_name is not False:
            kwargs['prog_is_name'] = self.prog_is_name
        if self.version is not None:
            kwargs['version'] = self.version
        return kwargs

    def __str__(self) -> str:
        return self.name  # not showing prog for root

    def configure_parser(self) -> None:
        """
        Configure the parser for this object. Typically not called by
        nor overridden in end-user code.
        """
        self.debug_print("Configuring root parser for '{self}'")
        parser_options: dict[str, Any] = {
            'description': self.__doc__,
            'allow_abbrev': False,
        }
        if self.prog_is_name:
            parser_options['prog'] = self.name
        parser_options |= self.parser_options()
        self._decree_parser = self.argument_parser_class(**parser_options)

    def parser_options(
        self,
        subparser: bool = False,  # pylint: disable=unused-argument
    ) -> dict[str, Any]:
        """
        Add to and override options passed to the argparse parser.

        :param subparser: whether the options are applied to a subparser
          applied via subparsers.add_parser() versus a top level parser initialization
        :returns: the options to provide to the parser
        """
        return {}

    def debug_print(self, message: str, **kwargs: Any) -> None:
        r"""
        Print an internal debug statement. Could be overridden to use logging.
        By default, expects message to support str.format() substitution,
        including the `self` variable.

        :param message: the message to print, using str.format() keywords
        :param \**kwargs: the arguments to specify to str.format() in addition to `self`
        """
        # FIXME consider using gettext for the callers
        if self.debug_tracing:
            final_message = message.format(self=self, **kwargs)
            print(final_message)

    def run(
        self,
        argv: Sequence[str] | None = None,
        options: argparse.Namespace | None = None,
        *,
        debug_tracing: bool = False,
        argument_parser_class: type[argparse.ArgumentParser] | None = None,
    ) -> Any:
        """
        Run the command by itself via command line or with defined arguments.

        :param argv: command-line arguments to parse
        :param options: processed arguments, circumventing parse_args if specified
        :param debug_tracing: whether to show debug tracing statements
        :param argument_parser_class: an override for the argument parser class
        :returns: the results, to facilitate testing
        """
        self.debug_tracing = debug_tracing
        self.debug_print("Running '{self}'")
        if argument_parser_class is not None:
            self.argument_parser_class = argument_parser_class
        if not hasattr(self, '_decree_parser'):
            self.configure_parser()
        self.add_arguments(self._decree_parser)
        self.preprocess_options(argv, options)
        self.process_options()
        return self.execute()

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """
        Add arguments to ``parser`` (not ``self._decree_parser``), if any.
        Subclass overrides typically include a call to ``super().add_arguments(parser)``.
        Handle manual argument processing in ``process_options``, not here.

        :param parser: the parser to which arguments will be added
        """
        self.debug_print("Adding arguments from '{self}' to parser")
        if self.version:
            parser.add_argument('--version', action='version',
                                version=f'%(prog)s {self.version}')

    def preprocess_options(self,
                           argv: Sequence[str] | None = None,
                           options: argparse.Namespace | None = None) -> None:
        """
        Populate ``self.options`` if it isn't already. Typically not called by
        nor overridden in end-user code.

        :param argv: command-line arguments to parse
        :param options: processed arguments, circumventing parse_args if specified
        """
        self.debug_print("Preprocessing options for '{self}'{from_opts}{options}",
                         from_opts=' from options: ' if options is not None else '',
                         options=options if options is not None else '')
        if options:
            self.debug_print("Copying args in '{self}'")
            for key, value in vars(options).items():
                # Keep self.options as the same object
                setattr(self.options, key, value)
        elif self.options == argparse.Namespace():
            if isinstance(argv, str):
                # Allow processing a string with all arguments
                argv = argv.split()
            self.debug_print("Parsing args in '{self}'")
            self._decree_parser.parse_args(argv, self.options)
        # Otherwise, use whatever is in ``self.options`` already
        self.debug_print("Found options '{self.options}'")

    def process_options(self) -> None:
        """
        Perform any needed processing on the options, prior to execution.
        Subclass overrides typically include a call to ``super().process_options()``.
        """
        self.debug_print("Processing options for '{self}'")

    def execute(self) -> Any:
        """
        Execute [sub]command processing.
        Subclass overrides typically include a call to ``super().execute()``.

        :returns: any required data
        """
        self.debug_print("Executing '{self}'")
