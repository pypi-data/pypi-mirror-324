import typing
import collections.abc
import typing_extensions
import bpy._typing.rna_enums
import bpy.ops.transform
import bpy.types

def brush_stroke(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    stroke: bpy.types.bpy_prop_collection[bpy.types.OperatorStrokeElement]
    | None = None,
    mode: typing.Literal["NORMAL", "INVERT", "SMOOTH"] | None = "NORMAL",
):
    """Draw a new stroke in the active Grease Pencil object

        :type execution_context: int | str | None
        :type undo: bool | None
        :param stroke: Stroke
        :type stroke: bpy.types.bpy_prop_collection[bpy.types.OperatorStrokeElement] | None
        :param mode: Stroke Mode, Action taken when a paint stroke is made

    NORMAL
    Regular -- Apply brush normally.

    INVERT
    Invert -- Invert action of brush for duration of stroke.

    SMOOTH
    Smooth -- Switch brush to smooth mode for duration of stroke.
        :type mode: typing.Literal['NORMAL','INVERT','SMOOTH'] | None
    """

def caps_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["ROUND", "FLAT", "START", "END"] | None = "ROUND",
):
    """Change curve caps mode (rounded or flat)

        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Type

    ROUND
    Rounded -- Set as default rounded.

    FLAT
    Flat.

    START
    Toggle Start.

    END
    Toggle End.
        :type type: typing.Literal['ROUND','FLAT','START','END'] | None
    """

def clean_loose(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    limit: int | None = 1,
):
    """Remove loose points

    :type execution_context: int | str | None
    :type undo: bool | None
    :param limit: Limit, Number of points to consider stroke as loose
    :type limit: int | None
    """

def cyclical_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["CLOSE", "OPEN", "TOGGLE"] | None = "TOGGLE",
):
    """Close or open the selected stroke adding a segment from last to first point

    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type
    :type type: typing.Literal['CLOSE','OPEN','TOGGLE'] | None
    """

def delete(execution_context: int | str | None = None, undo: bool | None = None):
    """Delete selected strokes or points

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def delete_frame(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["ACTIVE_FRAME", "ALL_FRAMES"] | None = "ACTIVE_FRAME",
):
    """Delete Grease Pencil Frame(s)

        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Type, Method used for deleting Grease Pencil frames

    ACTIVE_FRAME
    Active Frame -- Deletes current frame in the active layer.

    ALL_FRAMES
    All Active Frames -- Delete active frames for all layers.
        :type type: typing.Literal['ACTIVE_FRAME','ALL_FRAMES'] | None
    """

def dissolve(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["POINTS", "BETWEEN", "UNSELECT"] | None = "POINTS",
):
    """Delete selected points without splitting strokes

        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Type, Method used for dissolving stroke points

    POINTS
    Dissolve -- Dissolve selected points.

    BETWEEN
    Dissolve Between -- Dissolve points between selected points.

    UNSELECT
    Dissolve Unselect -- Dissolve all unselected points.
        :type type: typing.Literal['POINTS','BETWEEN','UNSELECT'] | None
    """

def draw_mode_toggle(
    execution_context: int | str | None = None, undo: bool | None = None
):
    """Enter/Exit draw mode for grease pencil

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def duplicate(execution_context: int | str | None = None, undo: bool | None = None):
    """Duplicate the selected points

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def duplicate_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    GREASE_PENCIL_OT_duplicate: typing.Any | None = None,
    TRANSFORM_OT_translate: bpy.ops.transform.translate | None = None,
):
    """Make copies of the selected Grease Pencil strokes and move them

    :type execution_context: int | str | None
    :type undo: bool | None
    :param GREASE_PENCIL_OT_duplicate: Duplicate, Duplicate the selected points
    :type GREASE_PENCIL_OT_duplicate: typing.Any | None
    :param TRANSFORM_OT_translate: Move, Move selected items
    :type TRANSFORM_OT_translate: bpy.ops.transform.translate | None
    """

def insert_blank_frame(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    all_layers: bool | None = False,
    duration: int | None = 0,
):
    """Insert a blank frame on the current scene frame

    :type execution_context: int | str | None
    :type undo: bool | None
    :param all_layers: All Layers, Insert a blank frame in all editable layers
    :type all_layers: bool | None
    :param duration: Duration
    :type duration: int | None
    """

def layer_active(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    layer: int | None = 0,
):
    """Set the active Grease Pencil layer

    :type execution_context: int | str | None
    :type undo: bool | None
    :param layer: Grease Pencil Layer
    :type layer: int | None
    """

def layer_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    new_layer_name: str = "Layer",
):
    """Add a new Grease Pencil layer in the active object

    :type execution_context: int | str | None
    :type undo: bool | None
    :param new_layer_name: Name, Name of the new layer
    :type new_layer_name: str
    """

def layer_group_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    new_layer_group_name: str = "",
):
    """Add a new Grease Pencil layer group in the active object

    :type execution_context: int | str | None
    :type undo: bool | None
    :param new_layer_group_name: Name, Name of the new layer group
    :type new_layer_group_name: str
    """

def layer_hide(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    unselected: bool | None = False,
):
    """Hide selected/unselected Grease Pencil layers

    :type execution_context: int | str | None
    :type undo: bool | None
    :param unselected: Unselected, Hide unselected rather than selected layers
    :type unselected: bool | None
    """

def layer_isolate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    affect_visibility: bool | None = False,
):
    """Make only active layer visible/editable

    :type execution_context: int | str | None
    :type undo: bool | None
    :param affect_visibility: Affect Visibility, Also affect the visibility
    :type affect_visibility: bool | None
    """

def layer_remove(execution_context: int | str | None = None, undo: bool | None = None):
    """Remove the active Grease Pencil layer

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def layer_reorder(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    target_layer_name: str = "Layer",
    location: typing.Literal["ABOVE", "BELOW"] | None = "ABOVE",
):
    """Reorder the active Grease Pencil layer

    :type execution_context: int | str | None
    :type undo: bool | None
    :param target_layer_name: Target Name, Name of the target layer
    :type target_layer_name: str
    :param location: Location
    :type location: typing.Literal['ABOVE','BELOW'] | None
    """

def layer_reveal(execution_context: int | str | None = None, undo: bool | None = None):
    """Show all Grease Pencil layers

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def material_copy_to_object(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    only_active: bool | None = True,
):
    """Append Materials of the active Grease Pencil to other object

    :type execution_context: int | str | None
    :type undo: bool | None
    :param only_active: Only Active, Append only active material, uncheck to append all materials
    :type only_active: bool | None
    """

def material_hide(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    invert: bool | None = False,
):
    """Hide active/inactive Grease Pencil material(s)

    :type execution_context: int | str | None
    :type undo: bool | None
    :param invert: Invert, Hide inactive materials instead of the active one
    :type invert: bool | None
    """

def material_lock_all(
    execution_context: int | str | None = None, undo: bool | None = None
):
    """Lock all Grease Pencil materials to prevent them from being accidentally modified

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def material_lock_unselected(
    execution_context: int | str | None = None, undo: bool | None = None
):
    """Lock any material not used in any selected stroke

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def material_lock_unused(
    execution_context: int | str | None = None, undo: bool | None = None
):
    """Lock and hide any material not used

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def material_reveal(
    execution_context: int | str | None = None, undo: bool | None = None
):
    """Unhide all hidden Grease Pencil materials

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def material_unlock_all(
    execution_context: int | str | None = None, undo: bool | None = None
):
    """Unlock all Grease Pencil materials so that they can be edited

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def move_to_layer(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    target_layer_name: str = "Layer",
    add_new_layer: bool | None = False,
):
    """Move selected strokes to another layer

    :type execution_context: int | str | None
    :type undo: bool | None
    :param target_layer_name: Name, Target Grease Pencil Layer
    :type target_layer_name: str
    :param add_new_layer: New Layer, Move selection to a new layer
    :type add_new_layer: bool | None
    """

def reorder(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["TOP", "UP", "DOWN", "BOTTOM"] | None = "TOP",
):
    """Change the display order of the selected strokes

    :type execution_context: int | str | None
    :type undo: bool | None
    :param direction: Direction
    :type direction: typing.Literal['TOP','UP','DOWN','BOTTOM'] | None
    """

def select_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    action: typing.Literal["TOGGLE", "SELECT", "DESELECT", "INVERT"] | None = "TOGGLE",
):
    """(De)select all visible strokes

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

def select_alternate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    deselect_ends: bool | None = False,
):
    """Select alternated points in strokes with already selected points

    :type execution_context: int | str | None
    :type undo: bool | None
    :param deselect_ends: Deselect Ends, (De)select the first and last point of each stroke
    :type deselect_ends: bool | None
    """

def select_ends(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    amount_start: int | None = 0,
    amount_end: int | None = 1,
):
    """Select end points of strokes

    :type execution_context: int | str | None
    :type undo: bool | None
    :param amount_start: Amount Start, Number of points to select from the start
    :type amount_start: int | None
    :param amount_end: Amount End, Number of points to select from the end
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
    ratio: float | None = 0.5,
    seed: int | None = 0,
    action: typing.Literal["SELECT", "DESELECT"] | None = "SELECT",
):
    """Selects random points from the current strokes selection

        :type execution_context: int | str | None
        :type undo: bool | None
        :param ratio: Ratio, Portion of items to select randomly
        :type ratio: float | None
        :param seed: Random Seed, Seed for the random number generator
        :type seed: int | None
        :param action: Action, Selection action to execute

    SELECT
    Select -- Select all elements.

    DESELECT
    Deselect -- Deselect all elements.
        :type action: typing.Literal['SELECT','DESELECT'] | None
    """

def separate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    mode: typing.Literal["SELECTED", "MATERIAL", "LAYER"] | None = "SELECTED",
):
    """Separate the selected geometry into a new grease pencil object

        :type execution_context: int | str | None
        :type undo: bool | None
        :param mode: Mode

    SELECTED
    Selection -- Separate selected geometry.

    MATERIAL
    By Material -- Separate by material.

    LAYER
    By Layer -- Separate by layer.
        :type mode: typing.Literal['SELECTED','MATERIAL','LAYER'] | None
    """

def set_active_material(
    execution_context: int | str | None = None, undo: bool | None = None
):
    """Set the selected stroke material as the active material

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def set_material(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    slot: str | None = "DEFAULT",
):
    """Set active material

    :type execution_context: int | str | None
    :type undo: bool | None
    :param slot: Material Slot
    :type slot: str | None
    """

def set_selection_mode(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    mode: bpy._typing.rna_enums.GreasePencilSelectmodeItems | None = "POINT",
):
    """Change the selection mode for Grease Pencil strokes

    :type execution_context: int | str | None
    :type undo: bool | None
    :param mode: Mode
    :type mode: bpy._typing.rna_enums.GreasePencilSelectmodeItems | None
    """

def set_uniform_opacity(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    opacity: float | None = 1.0,
):
    """Set all stroke points to same opacity

    :type execution_context: int | str | None
    :type undo: bool | None
    :param opacity: Opacity
    :type opacity: float | None
    """

def set_uniform_thickness(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    thickness: float | None = 0.1,
):
    """Set all stroke points to same thickness

    :type execution_context: int | str | None
    :type undo: bool | None
    :param thickness: Thickness, Thickness
    :type thickness: float | None
    """

def stroke_material_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    material: str = "",
):
    """Assign the active material slot to the selected strokes

    :type execution_context: int | str | None
    :type undo: bool | None
    :param material: Material, Name of the material
    :type material: str
    """

def stroke_simplify(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    factor: float | None = 0.01,
):
    """Simplify selected strokes

    :type execution_context: int | str | None
    :type undo: bool | None
    :param factor: Factor
    :type factor: float | None
    """

def stroke_smooth(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    iterations: int | None = 10,
    factor: float | None = 1.0,
    smooth_ends: bool | None = False,
    keep_shape: bool | None = False,
    smooth_position: bool | None = True,
    smooth_radius: bool | None = True,
    smooth_opacity: bool | None = False,
):
    """Smooth selected strokes

    :type execution_context: int | str | None
    :type undo: bool | None
    :param iterations: Iterations
    :type iterations: int | None
    :param factor: Factor
    :type factor: float | None
    :param smooth_ends: Smooth Endpoints
    :type smooth_ends: bool | None
    :param keep_shape: Keep Shape
    :type keep_shape: bool | None
    :param smooth_position: Position
    :type smooth_position: bool | None
    :param smooth_radius: Radius
    :type smooth_radius: bool | None
    :param smooth_opacity: Opacity
    :type smooth_opacity: bool | None
    """

def stroke_subdivide(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    number_cuts: int | None = 1,
    only_selected: bool | None = True,
):
    """Subdivide between continuous selected points of the stroke adding a point half way between them

    :type execution_context: int | str | None
    :type undo: bool | None
    :param number_cuts: Number of Cuts
    :type number_cuts: int | None
    :param only_selected: Selected Points, Smooth only selected points in the stroke
    :type only_selected: bool | None
    """

def stroke_subdivide_smooth(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    GREASE_PENCIL_OT_stroke_subdivide: typing.Any | None = None,
    GREASE_PENCIL_OT_stroke_smooth: typing.Any | None = None,
):
    """Subdivide strokes and smooth them

    :type execution_context: int | str | None
    :type undo: bool | None
    :param GREASE_PENCIL_OT_stroke_subdivide: Subdivide Stroke, Subdivide between continuous selected points of the stroke adding a point half way between them
    :type GREASE_PENCIL_OT_stroke_subdivide: typing.Any | None
    :param GREASE_PENCIL_OT_stroke_smooth: Smooth Stroke, Smooth selected strokes
    :type GREASE_PENCIL_OT_stroke_smooth: typing.Any | None
    """

def stroke_switch_direction(
    execution_context: int | str | None = None, undo: bool | None = None
):
    """Change direction of the points of the selected strokes

    :type execution_context: int | str | None
    :type undo: bool | None
    """
