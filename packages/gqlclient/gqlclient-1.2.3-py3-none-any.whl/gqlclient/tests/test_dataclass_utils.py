"""
Test dataclass_utils
"""
from dataclasses import dataclass
from typing import Annotated
from typing import Any
from typing import ForwardRef
from typing import Optional
from typing import Union

import pytest
from dacite.types import is_optional
from dacite.types import is_union

from gqlclient.dataclass_utils import extract_dataclass
from gqlclient.dataclass_utils import yield_valid_fields
from gqlclient.pydantic_utils import builtin_dc_name
from gqlclient.pydantic_version_util import PYDANTIC_LOADED
from gqlclient.tests.test_utils import assert_fields_match

# valid explicit forward references
BuiltinRef = ForwardRef("Builtin", module=__name__)
PydanticRef = ForwardRef("Pydantic", module=__name__)
BasemodelRef = ForwardRef("Basemodel", module=__name__)


@dataclass
class BuiltinWithForwardRef:
    parent_ref: list[BuiltinRef]
    value: str = "builtin with forward ref"


@dataclass
class Builtin:
    child_ref: BuiltinWithForwardRef
    value: str = "builtin dataclass"


if PYDANTIC_LOADED:
    from pydantic import StrictBool  # noqa
    from pydantic import StrictBytes  # noqa
    from pydantic import StrictFloat  # noqa
    from pydantic import StrictInt  # noqa
    from pydantic import StrictStr  # noqa
    from pydantic.dataclasses import dataclass as pydantic_dataclass  # noqa
    from pydantic import BaseModel  # noqa

    @pydantic_dataclass
    class PydanticWithForwardRef:
        parent_ref: list[PydanticRef]
        value: str = "pydantic with forward ref"

    @pydantic_dataclass
    class Pydantic:
        child_ref: PydanticWithForwardRef
        value: str = "pydantic"

    class BasemodelWithForwardRef(BaseModel):
        parent_ref: list[BasemodelRef]
        value: str = "basemodel with forward ref"

    class Basemodel(BaseModel):
        child_ref: BasemodelWithForwardRef
        value: str = "basemodel"

    @dataclass
    class BuiltinWithAnnotatedTypes:
        strict_str: StrictStr
        strict_int: StrictInt
        strict_bool: StrictBool
        strict_bytes: StrictBytes
        strict_float: StrictFloat
        annotated_dc: Annotated[Builtin, "interesting metadata"]
        value: str = "builtin with annotated types"

    @pydantic_dataclass
    class PydanticWithAnnotatedTypes:
        strict_str: StrictStr
        strict_int: StrictInt
        strict_bool: StrictBool
        strict_bytes: StrictBytes
        strict_float: StrictFloat
        annotated_dc: Annotated[Pydantic, "boring meta"]
        value: str = "pydantic with annotated types"

    class BasemodelWithAnnotatedTypes(BaseModel):
        strict_str: StrictStr
        strict_int: StrictInt
        strict_bool: StrictBool
        strict_bytes: StrictBytes
        strict_float: StrictFloat
        annotated_dc: Annotated[Basemodel, "neglected meta"]
        value: str = "basemodel with annotated types"


def params_is_optional() -> list[pytest.param]:
    """
    test_type, expected_result
    Used by `test_is_optional`
    """
    params = [
        pytest.param(Optional[str], True, id="old_opt"),
        pytest.param(Union[str, None], True, id="old_union"),
        pytest.param(str | None, True, id="new_union"),
        pytest.param(str, False, id="str"),
        pytest.param(str | bool, False, id="str_bool"),
        pytest.param(Builtin | bool, False, id="new_builtin_bool"),
        pytest.param(Builtin | None, True, id="new_builtin_none"),
        pytest.param(Union[Builtin, bool], False, id="old_builtin_bool"),
        pytest.param(Union[Builtin, None], True, id="old_builtin_none"),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(Pydantic | bool, False, id="new_pyd_bool"),
                pytest.param(Pydantic | None, True, id="new_pyd_none"),
                pytest.param(Union[Pydantic, bool], False, id="old_pyd_bool"),
                pytest.param(Union[Pydantic, None], True, id="old_pyd_none"),
                pytest.param(Builtin | Pydantic, False, id="new_builtin_pyd"),
                pytest.param(Union[Builtin, Pydantic], False, id="old_builtin_pyd"),
                pytest.param(Basemodel | bool, False, id="new_basemodel_bool"),
                pytest.param(Basemodel | None, True, id="new_basemodel_none"),
                pytest.param(Union[Basemodel, bool], False, id="old_basemodel_bool"),
                pytest.param(Union[Basemodel, None], True, id="old_basemodel_none"),
                pytest.param(Builtin | Basemodel, False, id="new_builtin_basemodel"),
                pytest.param(Union[Builtin, Basemodel], False, id="old_builtin_basemodel"),
            ]
        )
    return params


@pytest.mark.parametrize("test_type, expected_result", params_is_optional())
def test_is_optional(test_type: type, expected_result: bool):
    """Verify stability of dacite behavior"""
    assert is_optional(test_type) == expected_result


def params_is_union() -> list[pytest.param]:
    """
    test_type, expected_result
    Used by `test_is_union`
    """
    params = [
        pytest.param(Optional[str], True, id="old_opt"),
        pytest.param(Union[str, None], True, id="old_union"),
        pytest.param(str | None, True, id="new_union"),
        pytest.param(str, False, id="str"),
        pytest.param(str | bool, True, id="str_bool"),
        pytest.param(Builtin | bool, True, id="new_builtin_bool"),
        pytest.param(Builtin | None, True, id="new_builtin_none"),
        pytest.param(Union[Builtin, bool], True, id="old_builtin_bool"),
        pytest.param(Union[Builtin, None], True, id="old_builtin_none"),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(Pydantic | bool, True, id="new_pyd_bool"),
                pytest.param(Pydantic | None, True, id="new_pyd_none"),
                pytest.param(Union[Pydantic, bool], True, id="old_pyd_bool"),
                pytest.param(Union[Pydantic, None], True, id="old_pyd_none"),
                pytest.param(Builtin | Pydantic, True, id="new_builtin_pyd"),
                pytest.param(Union[Builtin, Pydantic], True, id="old_builtin_pyd"),
                pytest.param(Basemodel | bool, True, id="new_basemodel_bool"),
                pytest.param(Basemodel | None, True, id="new_basemodel_none"),
                pytest.param(Union[Basemodel, bool], True, id="old_basemodel_bool"),
                pytest.param(Union[Basemodel, None], True, id="old_basemodel_none"),
                pytest.param(Builtin | Basemodel, True, id="new_builtin_basemodel"),
                pytest.param(Union[Builtin, Basemodel], True, id="old_builtin_basemodel"),
            ]
        )
    return params


@pytest.mark.parametrize("test_type, expected_result", params_is_union())
def test_is_union(test_type: type, expected_result: bool):
    """Verify stability of dacite behavior"""
    assert is_union(test_type) == expected_result


def params_extract_dataclass_simple() -> list[pytest.param]:
    """
    test_type, expected_result
    Used by `test_extract_dataclass_simple`
    """
    params = [
        pytest.param(Optional[str], None, id="old_opt"),
        pytest.param(Union[str, None], None, id="old_union"),
        pytest.param(str | None, None, id="new_union"),
        pytest.param(str, None, id="str"),
        pytest.param(str | bool, None, id="str_bool"),
        pytest.param(Builtin | bool, Builtin, id="new_builtin_bool"),
        pytest.param(Builtin | None, Builtin, id="new_builtin_none"),
        pytest.param(Union[Builtin, bool], Builtin, id="old_builtin_bool"),
        pytest.param(Union[Builtin, None], Builtin, id="old_builtin_none"),
        pytest.param(Annotated[str, "metadata"], None, id="annotated_str"),
        pytest.param(Annotated[int, "metadata"], None, id="annotated_int"),
        pytest.param(Annotated[bool, "metadata"], None, id="annotated_bool"),
        pytest.param(Annotated[Builtin, "metadata"], Builtin, id="annotated_builtin"),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(Pydantic | bool, Pydantic, id="new_pyd_bool"),
                pytest.param(Pydantic | None, Pydantic, id="new_pyd_none"),
                pytest.param(Union[Pydantic, bool], Pydantic, id="old_pyd_bool"),
                pytest.param(Union[Pydantic, None], Pydantic, id="old_pyd_none"),
                pytest.param(Annotated[Pydantic, "metadata"], Pydantic, id="annotated_pyd"),
            ]
        )
    return params


@pytest.mark.parametrize("test_type, expected_result", params_extract_dataclass_simple())
def test_extract_dataclass_simple(test_type: type, expected_result: Any):
    """Verify proper dataclass extraction"""
    assert extract_dataclass(test_type) == expected_result


def params_extract_dataclass_simple_basemodel() -> list[pytest.param]:
    """
    test_type, equivalent
    Used by `test_extract_dataclass_simple_basemodel`
    """
    params = []
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(Basemodel | bool, Basemodel, id="new_basemodel_bool"),
                pytest.param(Basemodel | None, Basemodel, id="new_basemodel_none"),
                pytest.param(Union[Basemodel, bool], Basemodel, id="old_basemodel_bool"),
                pytest.param(Union[Basemodel, None], Basemodel, id="old_basemodel_none"),
                pytest.param(Annotated[Basemodel, "metadata"], Basemodel, id="annotated_basemodel"),
            ]
        )
    return params


@pytest.mark.parametrize("test_type, equivalent", params_extract_dataclass_simple_basemodel())
def test_extract_dataclass_simple_basemodel(test_type: type, equivalent: Any):
    """Verify proper dataclass extraction"""
    # won't be the same type for BaseModel because a BaseModel will get converted to a builtin dataclass
    actual_result = extract_dataclass(test_type)
    expected_name = equivalent.__name__
    actual_name = actual_result.__name__
    assert builtin_dc_name(expected_name) == actual_name
    assert_fields_match(actual_result, equivalent)


def params_extract_dataclass_multi() -> list[pytest.param]:
    """
    test_type
    Used by `test_extract_dataclass_multi`
    """
    params = []
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(Builtin | Pydantic, id="new_builtin_pyd"),
                pytest.param(Union[Builtin, Pydantic], id="old_builtin_pyd"),
                pytest.param(Pydantic | Basemodel, id="new_pyd_basemodel"),
                pytest.param(Union[Pydantic, Basemodel], id="old_pyd_basemodel"),
                pytest.param(Builtin | Basemodel, id="new_builtin_basemodel"),
                pytest.param(Union[Builtin, Basemodel], id="old_builtin_basemodel"),
            ]
        )
    return params


@pytest.mark.parametrize("test_type", params_extract_dataclass_multi())
def test_extract_dataclass_multi(test_type: type):
    """Raise exception when a field has multiple possible dataclasses"""
    with pytest.raises(ValueError):
        extract_dataclass(test_type)


def params_extract_dataclass_forward_ref_explicit() -> list[pytest.param]:
    """
    test_type, expected_result
    Used by `test_extract_dataclass_forward_ref_explicit`
    """
    params = [
        pytest.param(BuiltinRef, Builtin, id="builtin"),
        pytest.param(Optional[BuiltinRef], Builtin, id="opt_builtin"),
        pytest.param(Union[BuiltinRef, None], Builtin, id="union_builtin"),
        pytest.param(list[BuiltinRef], Builtin, id="list_builtin"),
        pytest.param(list[Optional[BuiltinRef]], Builtin, id="list_opt_builtin"),
        pytest.param(list[Union[BuiltinRef, bool]], Builtin, id="list_union_builtin"),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(PydanticRef, Pydantic, id="pyd"),
                pytest.param(Optional[PydanticRef], Pydantic, id="opt_pyd"),
                pytest.param(Union[PydanticRef, None], Pydantic, id="union_pyd"),
                pytest.param(list[PydanticRef], Pydantic, id="list_pyd"),
                pytest.param(list[Optional[PydanticRef]], Pydantic, id="list_opt_pyd"),
                pytest.param(list[Union[PydanticRef, bool]], Pydantic, id="list_union_pyd"),
            ]
        )
    return params


@pytest.mark.parametrize(
    "test_type, expected_result", params_extract_dataclass_forward_ref_explicit()
)
def test_extract_dataclass_forward_ref_explicit(test_type: type, expected_result: Any):
    """Verify proper dataclass extraction from ForwardRefs"""
    assert extract_dataclass(test_type) == expected_result


def params_extract_dataclass_forward_ref_explicit_basemodel() -> list[pytest.param]:
    """
    test_type, equivalent
    Used by `test_extract_dataclass_forward_ref_explicit_basemodel`
    """
    params = []
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(BasemodelRef, Basemodel, id="basemodel"),
                pytest.param(Optional[BasemodelRef], Basemodel, id="opt_basemodel"),
                pytest.param(Union[BasemodelRef, None], Basemodel, id="union_basemodel"),
                pytest.param(list[BasemodelRef], Basemodel, id="list_basemodel"),
                pytest.param(list[Optional[BasemodelRef]], Basemodel, id="list_opt_basemodel"),
                pytest.param(list[Union[BasemodelRef, bool]], Basemodel, id="list_union_basemodel"),
            ]
        )
    return params


@pytest.mark.parametrize(
    "test_type, equivalent", params_extract_dataclass_forward_ref_explicit_basemodel()
)
def test_extract_dataclass_forward_ref_explicit_basemodel(test_type: type, equivalent: Any):
    """Verify proper dataclass extraction from ForwardRefs"""
    actual_result = extract_dataclass(test_type)
    # actual result will be a builtin (annotated) dataclass, not a BaseModel
    assert_fields_match(actual_result, equivalent)


def params_extract_dataclass_forward_ref_implicit() -> list[pytest.param]:
    """
    test_type
    Used by `test_extract_dataclass_forward_ref_implicit`
    """
    params = [
        pytest.param(Optional["Builtin"], id="opt_builtin"),
        pytest.param(Union["Builtin", None], id="union_builtin"),
        pytest.param(list["Builtin"], id="list_builtin"),
        pytest.param(list[Optional["Builtin"]], id="list_opt_builtin"),
        pytest.param(list[Union["Builtin", bool]], id="list_union_builtin"),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(Optional["Pydantic"], id="opt_pyd"),
                pytest.param(Union["Pydantic", None], id="union_pyd"),
                pytest.param(list["Pydantic"], id="list_pyd"),
                pytest.param(list[Optional["Pydantic"]], id="list_opt_pyd"),
                pytest.param(list[Union["Pydantic", bool]], id="list_union_pyd"),
                pytest.param(Optional["Basemodel"], id="opt_basemodel"),
                pytest.param(Union["Basemodel", None], id="union_basemodel"),
                pytest.param(list["Basemodel"], id="list_basemodel"),
                pytest.param(list[Optional["Basemodel"]], id="list_opt_basemodel"),
                pytest.param(list[Union["Basemodel", bool]], id="list_union_basemodel"),
            ]
        )
    return params


@pytest.mark.parametrize("test_type", params_extract_dataclass_forward_ref_implicit())
def test_extract_dataclass_forward_ref_implicit(test_type: type):
    """Verify error if an implicit ForwardRef is wrapped by another data type"""
    with pytest.raises(ValueError):
        extract_dataclass(test_type)


def params_extract_dataclass_forward_ref_module() -> list[pytest.param]:
    """
    test_type
    Used by `test_extract_dataclass_forward_ref_module`
    """
    params = [
        pytest.param(ForwardRef("Builtin"), id="builtin_none"),
        pytest.param(ForwardRef("Builtin", module="abc"), id="builtin_abc"),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(ForwardRef("Pydantic"), id="pyd_none"),
                pytest.param(ForwardRef("Pydantic", module="abc"), id="pyd_abc"),
                pytest.param(ForwardRef("Basemodel"), id="basemodel_none"),
                pytest.param(ForwardRef("Basemodel", module="abc"), id="basemodel_abc"),
            ]
        )
    return params


@pytest.mark.parametrize("test_type", params_extract_dataclass_forward_ref_module())
def test_extract_dataclass_forward_ref_module(test_type: type):
    """Verify error if ForwardRef has missing or invalid module attribute"""
    with pytest.raises(ValueError):
        extract_dataclass(test_type)


def params_yield_valid_fields() -> list[pytest.param]:
    """
    test_type, test_context, expected_result
    Used by `test_yield_valid_fields`
    """
    params = [
        pytest.param(Builtin, None, {"child_ref", "value"}, id="builtin_parent_plain"),
        pytest.param(
            BuiltinWithForwardRef, None, {"parent_ref", "value"}, id="builtin_child_plain"
        ),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(Pydantic, None, {"child_ref", "value"}, id="pyd_parent_plain"),
                pytest.param(
                    PydanticWithForwardRef, None, {"parent_ref", "value"}, id="pyd_child_plain"
                ),
                pytest.param(Basemodel, None, {"child_ref", "value"}, id="basemodel_parent_plain"),
                pytest.param(
                    BasemodelWithForwardRef,
                    None,
                    {"parent_ref", "value"},
                    id="basemodel_child_plain",
                ),
                pytest.param(
                    BuiltinWithAnnotatedTypes,
                    None,
                    {
                        "strict_str",
                        "strict_int",
                        "strict_bool",
                        "strict_bytes",
                        "strict_float",
                        "annotated_dc",
                        "value",
                    },
                    id="builtin_annotated",
                ),
                pytest.param(
                    PydanticWithAnnotatedTypes,
                    None,
                    {
                        "strict_str",
                        "strict_int",
                        "strict_bool",
                        "strict_bytes",
                        "strict_float",
                        "annotated_dc",
                        "value",
                    },
                    id="pyd_annotated",
                ),
                pytest.param(
                    BasemodelWithAnnotatedTypes,
                    None,
                    {
                        "strict_str",
                        "strict_int",
                        "strict_bool",
                        "strict_bytes",
                        "strict_float",
                        "annotated_dc",
                        "value",
                    },
                    id="basemodel_annotated",
                ),
            ]
        )
    return params


@pytest.mark.parametrize("test_type, test_context, expected_result", params_yield_valid_fields())
def test_yield_valid_fields(
    test_type: type,
    test_context: set[str] | str | None,
    expected_result: set[str],
):
    """Verify the fields of the dataclass are returned"""
    fields = {field.name for field in yield_valid_fields(test_type, test_context)}
    assert fields == expected_result


def params_yield_valid_fields_circular() -> list[pytest.param]:
    """
    test_type, test_context
    Used by `test_yield_valid_fields_circular`
    """
    params = [
        pytest.param(Builtin, "BuiltinWithForwardRef", id="builtin_parent_context"),
        pytest.param(BuiltinWithForwardRef, {"Builtin"}, id="builtin_child_context"),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(Pydantic, "PydanticWithForwardRef", id="pyd_parent_context"),
                pytest.param(PydanticWithForwardRef, {"Pydantic"}, id="pyd_child_context"),
                pytest.param(
                    Basemodel,
                    builtin_dc_name("BasemodelWithForwardRef"),
                    id="basemodel_parent_context",
                ),
                pytest.param(
                    BasemodelWithForwardRef,
                    {builtin_dc_name("Basemodel")},
                    id="basemodel_child_context",
                ),
            ]
        )
    return params


@pytest.mark.parametrize("test_type, test_context", params_yield_valid_fields_circular())
def test_yield_valid_fields_circular(
    test_type: type,
    test_context: set[str] | str | None,
):
    """Verify an exception is raised to avoid infinite recursion caused by circular references"""
    with pytest.raises(ValueError):
        fields = {field.name for field in yield_valid_fields(test_type, test_context)}
