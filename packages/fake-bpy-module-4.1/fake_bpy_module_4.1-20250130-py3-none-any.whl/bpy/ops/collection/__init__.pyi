import typing
import collections.abc
import typing_extensions

def create(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str = "Collection",
):
    """Create an object collection from selected objects

    :type execution_context: int | str | None
    :type undo: bool | None
    :param name: Name, Name of the new collection
    :type name: str
    """

def objects_add_active(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    collection: str | None = "",
):
    """Add the object to an object collection that contains the active object

    :type execution_context: int | str | None
    :type undo: bool | None
    :param collection: Collection, The collection to add other selected objects to
    :type collection: str | None
    """

def objects_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    collection: str | None = "",
):
    """Remove selected objects from a collection

    :type execution_context: int | str | None
    :type undo: bool | None
    :param collection: Collection, The collection to remove this object from
    :type collection: str | None
    """

def objects_remove_active(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    collection: str | None = "",
):
    """Remove the object from an object collection that contains the active object

    :type execution_context: int | str | None
    :type undo: bool | None
    :param collection: Collection, The collection to remove other selected objects from
    :type collection: str | None
    """

def objects_remove_all(
    execution_context: int | str | None = None, undo: bool | None = None
):
    """Remove selected objects from all collections

    :type execution_context: int | str | None
    :type undo: bool | None
    """
