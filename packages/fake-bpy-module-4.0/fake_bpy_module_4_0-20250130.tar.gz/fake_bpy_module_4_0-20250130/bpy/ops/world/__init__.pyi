import typing
import collections.abc
import typing_extensions

def new(execution_context: int | str | None = None, undo: bool | None = None):
    """Create a new world Data-Block

    :type execution_context: int | str | None
    :type undo: bool | None
    """
