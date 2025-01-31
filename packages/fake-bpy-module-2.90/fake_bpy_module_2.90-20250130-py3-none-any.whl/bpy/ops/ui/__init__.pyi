import typing
import collections.abc
import typing_extensions
import bpy.types

def assign_default_button(
    override_context: bpy.types.Context | dict[str, typing.Any] = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Set this property's current value as the new default

    :type override_context: bpy.types.Context | dict[str, typing.Any]
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def button_execute(
    override_context: bpy.types.Context | dict[str, typing.Any] = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    skip_depressed: bool | None = False,
):
    """Presses active button

    :type override_context: bpy.types.Context | dict[str, typing.Any]
    :type execution_context: int | str | None
    :type undo: bool | None
    :param skip_depressed: Skip Depressed
    :type skip_depressed: bool | None
    """

def button_string_clear(
    override_context: bpy.types.Context | dict[str, typing.Any] = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Unsets the text of the active button

    :type override_context: bpy.types.Context | dict[str, typing.Any]
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def copy_as_driver_button(
    override_context: bpy.types.Context | dict[str, typing.Any] = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Create a new driver with this property as input, and copy it to the clipboard. Use Paste Driver to add it to the target property, or Paste Driver Variables to extend an existing driver

    :type override_context: bpy.types.Context | dict[str, typing.Any]
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def copy_data_path_button(
    override_context: bpy.types.Context | dict[str, typing.Any] = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    full_path: bool | None = False,
):
    """Copy the RNA data path for this property to the clipboard

    :type override_context: bpy.types.Context | dict[str, typing.Any]
    :type execution_context: int | str | None
    :type undo: bool | None
    :param full_path: full_path, Copy full data path
    :type full_path: bool | None
    """

def copy_python_command_button(
    override_context: bpy.types.Context | dict[str, typing.Any] = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Copy the Python command matching this button

    :type override_context: bpy.types.Context | dict[str, typing.Any]
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def copy_to_selected_button(
    override_context: bpy.types.Context | dict[str, typing.Any] = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    all: bool | None = True,
):
    """Copy property from this object to selected objects or bones

    :type override_context: bpy.types.Context | dict[str, typing.Any]
    :type execution_context: int | str | None
    :type undo: bool | None
    :param all: All, Copy to selected all elements of the array
    :type all: bool | None
    """

def drop_color(
    override_context: bpy.types.Context | dict[str, typing.Any] = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    color: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    gamma: bool | None = False,
):
    """Drop colors to buttons

    :type override_context: bpy.types.Context | dict[str, typing.Any]
    :type execution_context: int | str | None
    :type undo: bool | None
    :param color: Color, Source color
    :type color: collections.abc.Iterable[float] | None
    :param gamma: Gamma Corrected, The source color is gamma corrected
    :type gamma: bool | None
    """

def editsource(
    override_context: bpy.types.Context | dict[str, typing.Any] = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Edit UI source code of the active button

    :type override_context: bpy.types.Context | dict[str, typing.Any]
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def edittranslation_init(
    override_context: bpy.types.Context | dict[str, typing.Any] = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Edit i18n in current language for the active button

    :type override_context: bpy.types.Context | dict[str, typing.Any]
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def eyedropper_color(
    override_context: bpy.types.Context | dict[str, typing.Any] = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    use_accumulate: bool | None = True,
):
    """Sample a color from the Blender window to store in a property

    :type override_context: bpy.types.Context | dict[str, typing.Any]
    :type execution_context: int | str | None
    :type undo: bool | None
    :param use_accumulate: Accumulate
    :type use_accumulate: bool | None
    """

def eyedropper_colorramp(
    override_context: bpy.types.Context | dict[str, typing.Any] = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Sample a color band

    :type override_context: bpy.types.Context | dict[str, typing.Any]
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def eyedropper_colorramp_point(
    override_context: bpy.types.Context | dict[str, typing.Any] = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Point-sample a color band

    :type override_context: bpy.types.Context | dict[str, typing.Any]
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def eyedropper_depth(
    override_context: bpy.types.Context | dict[str, typing.Any] = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Sample depth from the 3D view

    :type override_context: bpy.types.Context | dict[str, typing.Any]
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def eyedropper_driver(
    override_context: bpy.types.Context | dict[str, typing.Any] = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    mapping_type: typing.Literal[
        "SINGLE_MANY", "DIRECT", "MATCH", "NONE_ALL", "NONE_SINGLE"
    ]
    | None = "SINGLE_MANY",
):
    """Pick a property to use as a driver target

        :type override_context: bpy.types.Context | dict[str, typing.Any]
        :type execution_context: int | str | None
        :type undo: bool | None
        :param mapping_type: Mapping Type, Method used to match target and driven properties

    SINGLE_MANY
    All from Target, Drive all components of this property using the target picked.

    DIRECT
    Single from Target, Drive this component of this property using the target picked.

    MATCH
    Match Indices, Create drivers for each pair of corresponding elements.

    NONE_ALL
    Manually Create Later, Create drivers for all properties without assigning any targets yet.

    NONE_SINGLE
    Manually Create Later (Single), Create driver for this property only and without assigning any targets yet.
        :type mapping_type: typing.Literal['SINGLE_MANY','DIRECT','MATCH','NONE_ALL','NONE_SINGLE'] | None
    """

def eyedropper_gpencil_color(
    override_context: bpy.types.Context | dict[str, typing.Any] = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    mode: typing.Literal["MATERIAL", "PALETTE"] | None = "MATERIAL",
):
    """Sample a color from the Blender Window and create Grease Pencil material

    :type override_context: bpy.types.Context | dict[str, typing.Any]
    :type execution_context: int | str | None
    :type undo: bool | None
    :param mode: Mode
    :type mode: typing.Literal['MATERIAL','PALETTE'] | None
    """

def eyedropper_id(
    override_context: bpy.types.Context | dict[str, typing.Any] = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Sample a data-block from the 3D View to store in a property

    :type override_context: bpy.types.Context | dict[str, typing.Any]
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def jump_to_target_button(
    override_context: bpy.types.Context | dict[str, typing.Any] = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Switch to the target object or bone

    :type override_context: bpy.types.Context | dict[str, typing.Any]
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def override_remove_button(
    override_context: bpy.types.Context | dict[str, typing.Any] = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    all: bool | None = True,
):
    """Remove an override operation

    :type override_context: bpy.types.Context | dict[str, typing.Any]
    :type execution_context: int | str | None
    :type undo: bool | None
    :param all: All, Reset to default values all elements of the array
    :type all: bool | None
    """

def override_type_set_button(
    override_context: bpy.types.Context | dict[str, typing.Any] = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    all: bool | None = True,
    type: typing.Literal["NOOP", "REPLACE", "DIFFERENCE", "FACTOR"] | None = "REPLACE",
):
    """Create an override operation, or set the type of an existing one

        :type override_context: bpy.types.Context | dict[str, typing.Any]
        :type execution_context: int | str | None
        :type undo: bool | None
        :param all: All, Reset to default values all elements of the array
        :type all: bool | None
        :param type: Type, Type of override operation

    NOOP
    NoOp, 'No-Operation', place holder preventing automatic override to ever affect the property.

    REPLACE
    Replace, Completely replace value from linked data by local one.

    DIFFERENCE
    Difference, Store difference to linked data value.

    FACTOR
    Factor, Store factor to linked data value (useful e.g. for scale).
        :type type: typing.Literal['NOOP','REPLACE','DIFFERENCE','FACTOR'] | None
    """

def reloadtranslation(
    override_context: bpy.types.Context | dict[str, typing.Any] = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Force a full reload of UI translation

    :type override_context: bpy.types.Context | dict[str, typing.Any]
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def reset_default_button(
    override_context: bpy.types.Context | dict[str, typing.Any] = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    all: bool | None = True,
):
    """Reset this property's value to its default value

    :type override_context: bpy.types.Context | dict[str, typing.Any]
    :type execution_context: int | str | None
    :type undo: bool | None
    :param all: All, Reset to default values all elements of the array
    :type all: bool | None
    """

def unset_property_button(
    override_context: bpy.types.Context | dict[str, typing.Any] = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Clear the property and use default or generated value in operators

    :type override_context: bpy.types.Context | dict[str, typing.Any]
    :type execution_context: int | str | None
    :type undo: bool | None
    """
