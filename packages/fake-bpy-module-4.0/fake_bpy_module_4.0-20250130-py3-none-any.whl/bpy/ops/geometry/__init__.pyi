import typing
import collections.abc
import typing_extensions
import bpy._typing.rna_enums

def attribute_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str = "Attribute",
    domain: bpy._typing.rna_enums.AttributeDomainItems | None = "POINT",
    data_type: bpy._typing.rna_enums.AttributeTypeItems | None = "FLOAT",
):
    """Add attribute to geometry

    :type execution_context: int | str | None
    :type undo: bool | None
    :param name: Name, Name of new attribute
    :type name: str
    :param domain: Domain, Type of element that attribute is stored on
    :type domain: bpy._typing.rna_enums.AttributeDomainItems | None
    :param data_type: Data Type, Type of data stored in attribute
    :type data_type: bpy._typing.rna_enums.AttributeTypeItems | None
    """

def attribute_convert(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    mode: typing.Literal["GENERIC", "VERTEX_GROUP"] | None = "GENERIC",
    domain: bpy._typing.rna_enums.AttributeDomainItems | None = "POINT",
    data_type: bpy._typing.rna_enums.AttributeTypeItems | None = "FLOAT",
):
    """Change how the attribute is stored

    :type execution_context: int | str | None
    :type undo: bool | None
    :param mode: Mode
    :type mode: typing.Literal['GENERIC','VERTEX_GROUP'] | None
    :param domain: Domain, Which geometry element to move the attribute to
    :type domain: bpy._typing.rna_enums.AttributeDomainItems | None
    :param data_type: Data Type
    :type data_type: bpy._typing.rna_enums.AttributeTypeItems | None
    """

def attribute_remove(
    execution_context: int | str | None = None, undo: bool | None = None
):
    """Remove attribute from geometry

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def color_attribute_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str = "Color",
    domain: bpy._typing.rna_enums.ColorAttributeDomainItems | None = "POINT",
    data_type: bpy._typing.rna_enums.ColorAttributeTypeItems | None = "FLOAT_COLOR",
    color: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0, 1.0),
):
    """Add color attribute to geometry

    :type execution_context: int | str | None
    :type undo: bool | None
    :param name: Name, Name of new color attribute
    :type name: str
    :param domain: Domain, Type of element that attribute is stored on
    :type domain: bpy._typing.rna_enums.ColorAttributeDomainItems | None
    :param data_type: Data Type, Type of data stored in attribute
    :type data_type: bpy._typing.rna_enums.ColorAttributeTypeItems | None
    :param color: Color, Default fill color
    :type color: collections.abc.Iterable[float] | None
    """

def color_attribute_convert(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    domain: bpy._typing.rna_enums.ColorAttributeDomainItems | None = "POINT",
    data_type: bpy._typing.rna_enums.ColorAttributeTypeItems | None = "FLOAT_COLOR",
):
    """Change how the color attribute is stored

    :type execution_context: int | str | None
    :type undo: bool | None
    :param domain: Domain, Type of element that attribute is stored on
    :type domain: bpy._typing.rna_enums.ColorAttributeDomainItems | None
    :param data_type: Data Type, Type of data stored in attribute
    :type data_type: bpy._typing.rna_enums.ColorAttributeTypeItems | None
    """

def color_attribute_duplicate(
    execution_context: int | str | None = None, undo: bool | None = None
):
    """Duplicate color attribute

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def color_attribute_remove(
    execution_context: int | str | None = None, undo: bool | None = None
):
    """Remove color attribute from geometry

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def color_attribute_render_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str = "Color",
):
    """Set default color attribute used for rendering

    :type execution_context: int | str | None
    :type undo: bool | None
    :param name: Name, Name of color attribute
    :type name: str
    """

def execute_node_group(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    asset_library_type: bpy._typing.rna_enums.AsetLibraryTypeItems | None = "LOCAL",
    asset_library_identifier: str = "",
    relative_asset_identifier: str = "",
    name: str = "",
    session_uuid: int | None = 0,
):
    """Execute a node group on geometry

    :type execution_context: int | str | None
    :type undo: bool | None
    :param asset_library_type: Asset Library Type
    :type asset_library_type: bpy._typing.rna_enums.AsetLibraryTypeItems | None
    :param asset_library_identifier: Asset Library Identifier
    :type asset_library_identifier: str
    :param relative_asset_identifier: Relative Asset Identifier
    :type relative_asset_identifier: str
    :param name: Name, Name of the data-block to use by the operator
    :type name: str
    :param session_uuid: Session UUID, Session UUID of the data-block to use by the operator
    :type session_uuid: int | None
    """

def geometry_randomization(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    value: bool | None = False,
):
    """Toggle geometry randomization for debugging purposes

    :type execution_context: int | str | None
    :type undo: bool | None
    :param value: Value, Randomize the order of geometry elements (e.g. vertices or edges) after some operations where there are no guarantees about the order. This avoids accidentally depending on something that may change in the future
    :type value: bool | None
    """
