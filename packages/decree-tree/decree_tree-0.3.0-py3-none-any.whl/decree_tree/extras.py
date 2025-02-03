"""DecreeTree subclasses with additional functionality."""

from typing import Any
from .assembled import DecreeTree
from .base import override


class AbstractDT(DecreeTree):
    """
    A mixin for creating abstract classes, which attempts to
    avoid issues resulting from mixing abstract with manual
    inheritance. Direct children of this class are also
    considered to be abstract.
    """

    # Make AbstractDT itself "abstract"
    name = ''
    help = ''

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        # Clear attributes from immediate child classes to make them "abstract".
        if AbstractDT in cls.__bases__:
            cls.name = ''
            cls.help = ''

    @override
    def parser_options(self, subparser: bool = False) -> dict[str, Any]:
        options = super().parser_options(subparser)
        # Have argparse attempt to resolve conflicting options,
        # including those that come from combinations of repeated
        # abstract classes and manual inheritance.
        options['conflict_handler'] = 'resolve'
        return options
