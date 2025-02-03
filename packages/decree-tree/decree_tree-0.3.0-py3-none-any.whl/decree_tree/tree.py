"""The multi-level tree."""

from typing import (
    Any, Callable, Generic, Type, TypeVar,
)
from .base import InvalidName, SupportsComparison


# A TypeVar for use in a generic type. If ignoring type-arg becomes
# problematic, consider using a recursive protocol definition per mypy docs.
T = TypeVar('T', bound='Tree')  # type: ignore[type-arg]


class Tree(Generic[T]):
    """Manage a generic tree structure."""

    def __init__(self, **kwargs: Any) -> None:
        r"""
        Initialize the tree structure.

        :param \**kwargs: any keyword arguments needed for subclass customization
        """
        super().__init__(**kwargs)
        # Intentionally making access slightly harder than just "_child" and "_parent"
        # to avoid single-character typos. Could use "__child" and "__parent", but
        # name mangling can be confusing if direct access is actually needed.
        self._children: list[T] = []
        self._parent: T | None = None
        # Not allowing a parent parameter for ``__init__``, since setting a parent
        # should be handled by ``append`` (etc.), which may get an initialized child
        # tree anyway.

    # Intentionally not overriding default Tree.__repr__() here

    def __str__(self) -> str:
        string = self.get_name
        if self.parent:
            string = ' -> '.join([str(self.parent), string])
        return string

    # FIXME add other methods? e.g. copy, deepcopy, extend, pop, reverse

    def append_child(self, child: T | Type[T]) -> T:
        """
        Append a new child.

        :param child: the object, class, or subclass to append
        :returns: the child itself, in case it was created within this method
        """
        if isinstance(child, type):
            child = child()
        child._parent = self  # pylint: disable=protected-access
        self._children.append(child)
        return child

    @property
    def children(self) -> list[T]:
        """
        Provide a copy of the child objects.
        This could be a generator, but since the list of
        children is expected to be short, there shouldn't be
        a need.

        :returns: the list of child instances
        """
        return list(self._children)

    def child_index(self, name: str, raise_exception: bool = False) -> int | None:
        """
        Determine the index of a child.

        :param name: the name of the child to look up
        :param raise_exception: whether to raise an exception if the child cannot be found
        :raises InvalidName: if the child cannot be found and raise_exception is True
        :returns: the index of the child or None if not found
        """
        for i, child in enumerate(self._children):
            if child.get_name == name:
                return i
        if raise_exception:
            raise InvalidName(f"Child of '{self.get_name}' with name '{name}' not found")
        return None

    @property
    def child_names(self) -> list[str]:
        """
        Provide a list of the names of the child
        objects. This could be a generator, but since the list of
        children is expected to be short, there shouldn't be
        a need.

        :returns: the list of the names of the child instances
        """
        # use of self.children matches parent_names
        return [child.get_name for child in self.children]

    def clear_children(self) -> None:
        """
        Clear the list of children.
        """
        for child in self._children:
            child._parent = None  # pylint: disable=protected-access
        self._children = []

    @property
    def count_children(self) -> int:
        """
        Provide the number of children.

        :returns: the number of children
        """
        return len(self._children)

    def find_child(self, name: str, raise_exception: bool = False) -> T | None:
        """
        Find a direct child by name and return it or None.

        :param name: the name of the child to find
        :param raise_exception: whether to raise an exception if the child cannot be found
        :raises InvalidName: if the child cannot be found and raise_exception is True
        :returns: the child or None if not found
        """
        for child in self._children:
            if child.get_name == name:
                return child
        if raise_exception:
            raise InvalidName(f"Child of '{self.get_name}' with name '{name}' not found")
        return None

    # Note that for a recursive tree, this should return ``T``, but
    # not sure how to correctly type this everywhere, e.g. for ``self``.
    # FIXME try to change this to return `T`
    def get_child(self, *args: str) -> 'Tree[T]':
        r"""
        Look up and provide the nested child object.

        :param \*args: the nested path of names to the requested object
        :raises InvalidName: if a matching object cannot be found
        :returns: the object found
        """
        try:
            name = args[0]
        except IndexError:
            return self
        if name == '':
            return self
        child = self.find_child(name)
        if not child:  # FIXME add raise_exception argument to this method?
            raise InvalidName(f"Item with path '{args}' not found in tree")
        try:
            _ = args[1]
        except IndexError:
            return child
        return child.get_child(*args[1:])

    @property
    def get_name(self) -> str:
        """
        A way to determine the "name" of an object. Rather than try to directly
        include the "name" variable from Decree in Tree, define
        a method that is intended to be overridden by a subclass. This method could
        perhaps be private, but that would force special handling in several
        Tree methods.

        :returns: the "name" of the instance
        """
        return repr(self)

    # FIXME add a way to get multiple children in chain
    # def get_children(self, *args: str) -> list[T]:
    #     ...

    # FIXME would it be better to have insert_before and insert_after?
    def insert_child(self, index: int, child: T | Type[T]) -> T:
        """
        Insert a new child.

        :param index: the position at which to insert the child
        :param child: the object, class, or subclass to insert
        :returns: the child object
        """
        if isinstance(child, type):
            child = child()
        child._parent = self  # pylint: disable=protected-access
        self._children.insert(index, child)  # FIXME may raise error for invalid index - doc this?
        return child

    @property
    def parent(self) -> T | None:
        """
        Return the parent of the object, if any.

        :returns: the parent object or None
        """
        return self._parent  # may be None

    @property
    def parents(self) -> list[T]:
        """
        Generate a list of the parents of this tree, in order.
        This could be a generator, but since the list of parents
        is expected to be short, there shouldn't be a need.

        :returns: the parents
        """
        if self._parent:
            parents = self._parent.parents
            parents.append(self._parent)
        else:
            parents = []
        return parents

    @property
    def parent_names(self) -> list[str]:
        """
        Generate a list of the names of the parents of this tree, in order.
        This could be a generator, but since the list of parents is
        expected to be short, there shouldn't be a need.

        :returns: the names of the parents
        """
        return [parent.get_name for parent in self.parents]

    def remove_child(self, name: str) -> None:
        """
        Remove a child.

        :param name: The name of the child to remove.
        """
        for index, child in enumerate(self._children):
            if child.get_name == name:
                self._children.pop(index)
                child._parent = None  # pylint: disable=protected-access
                break

    def replace_child(self,
                      name: str,  # FIXME optionally allow an object? and/or an int?
                      child: T | Type[T],
                      raise_exception: bool = False,
                      ) -> T | None:
        """
        Replace a child.

        :param name: the name of the child to replace
        :param child: the new object, class, or subclass
        :param raise_exception: the raise_exception argument to the index() call
        :returns: the instantiated child object
        """
        if isinstance(child, type):
            child = child()
        child._parent = self  # pylint: disable=protected-access
        i = self.child_index(name, raise_exception=raise_exception)
        if i is not None:
            if self._children[i]:  # should always be True
                self._children[i]._parent = None  # pylint: disable=protected-access
            self._children[i] = child
            return child
        return None

    def sort_children(self, *,
                      key: Callable[[T], SupportsComparison] | None = None,
                      reverse: bool = False) -> None:
        """
        Alphabetically sort the list of subcommands in place.

        :param key: a single-argument function used to extract the comparison key for each child
        :param reverse: whether to sort in reverse
        """
        self._children.sort(
            key=(lambda child: key(child) if key is not None else child.get_name),
            reverse=reverse,
        )
