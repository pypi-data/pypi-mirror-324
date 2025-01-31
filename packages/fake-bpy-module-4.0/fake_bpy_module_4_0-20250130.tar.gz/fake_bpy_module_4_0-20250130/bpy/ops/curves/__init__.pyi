import typing
import collections.abc
import typing_extensions
import bpy._typing.rna_enums

def convert_from_particle_system(
    execution_context: int | str | None = None, undo: bool | None = None
):
    """Add a new curves object based on the current state of the particle system

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def convert_to_particle_system(
    execution_context: int | str | None = None, undo: bool | None = None
):
    """Add a new or update an existing hair particle system on the surface object

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def delete(execution_context: int | str | None = None, undo: bool | None = None):
    """Remove selected control points or curves

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def sculptmode_toggle(
    execution_context: int | str | None = None, undo: bool | None = None
):
    """Enter/Exit sculpt mode for curves

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def select_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    action: typing.Literal["TOGGLE", "SELECT", "DESELECT", "INVERT"] | None = "TOGGLE",
):
    """(De)select all control points

        :type execution_context: int | str | None
        :type undo: bool | None
        :param action: Action, Selection action to execute

    TOGGLE
    Toggle -- Toggle selection for all elements.

    SELECT
    Select -- Select all elements.

    DESELECT
    Deselect -- Deselect all elements.

    INVERT
    Invert -- Invert selection of all elements.
        :type action: typing.Literal['TOGGLE','SELECT','DESELECT','INVERT'] | None
    """

def select_ends(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    amount_start: int | None = 0,
    amount_end: int | None = 1,
):
    """Select end points of curves

    :type execution_context: int | str | None
    :type undo: bool | None
    :param amount_start: Amount Front, Number of points to select from the front
    :type amount_start: int | None
    :param amount_end: Amount Back, Number of points to select from the back
    :type amount_end: int | None
    """

def select_less(execution_context: int | str | None = None, undo: bool | None = None):
    """Shrink the selection by one point

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def select_linked(execution_context: int | str | None = None, undo: bool | None = None):
    """Select all points in curves with any point selection

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def select_more(execution_context: int | str | None = None, undo: bool | None = None):
    """Grow the selection by one point

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def select_random(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    seed: int | None = 0,
    probability: float | None = 0.5,
):
    """Randomizes existing selection or create new random selection

    :type execution_context: int | str | None
    :type undo: bool | None
    :param seed: Seed, Source of randomness
    :type seed: int | None
    :param probability: Probability, Chance of every point or curve being included in the selection
    :type probability: float | None
    """

def set_selection_domain(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    domain: bpy._typing.rna_enums.AttributeCurvesDomainItems | None = "POINT",
):
    """Change the mode used for selection masking in curves sculpt mode

    :type execution_context: int | str | None
    :type undo: bool | None
    :param domain: Domain
    :type domain: bpy._typing.rna_enums.AttributeCurvesDomainItems | None
    """

def snap_curves_to_surface(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    attach_mode: typing.Literal["NEAREST", "DEFORM"] | None = "NEAREST",
):
    """Move curves so that the first point is exactly on the surface mesh

        :type execution_context: int | str | None
        :type undo: bool | None
        :param attach_mode: Attach Mode, How to find the point on the surface to attach to

    NEAREST
    Nearest -- Find the closest point on the surface for the root point of every curve and move the root there.

    DEFORM
    Deform -- Re-attach curves to a deformed surface using the existing attachment information. This only works when the topology of the surface mesh has not changed.
        :type attach_mode: typing.Literal['NEAREST','DEFORM'] | None
    """

def surface_set(execution_context: int | str | None = None, undo: bool | None = None):
    """Use the active object as surface for selected curves objects and set it as the parent

    :type execution_context: int | str | None
    :type undo: bool | None
    """
