"""
Test pydantic_utils
"""
from dataclasses import dataclass
from dataclasses import field
from dataclasses import is_dataclass
from datetime import datetime
from types import NoneType
from typing import Annotated
from typing import Any
from typing import ForwardRef
from uuid import uuid4

import pytest

from gqlclient.pydantic_utils import builtin_dc_name
from gqlclient.pydantic_utils import get_type
from gqlclient.pydantic_utils import is_basemodel
from gqlclient.pydantic_utils import to_builtin_dc
from gqlclient.pydantic_version_util import PYDANTIC_LOADED
from gqlclient.pydantic_version_util import PYDANTIC_VERSION
from gqlclient.tests.test_utils import assert_fields_match

# valid explicit forward references
BuiltinRef = ForwardRef("Builtin", module=__name__)
PydanticRef = ForwardRef("Pydantic", module=__name__)
BasemodelRef = ForwardRef("Basemodel", module=__name__)


@dataclass
class Builtin:
    str_param: str
    int_param: int
    float_param: float
    str_array_param: list[str]
    num_array_param: list[int]
    bool_param: bool
    date_param: datetime
    optional_int_param: int | None = None
    optional_list_param: list[str] | None = field(default_factory=list)


builtin = Builtin(
    str_param="A",
    int_param=1,
    float_param=1.1,
    str_array_param=["A", "B"],
    num_array_param=[1, 2],
    bool_param=False,
    date_param=datetime.strptime("2010-03-25T14:08:00", "%Y-%m-%dT%H:%M:%S"),
)


if PYDANTIC_LOADED:
    from pydantic import StrictBool  # noqa
    from pydantic import StrictBytes  # noqa
    from pydantic import StrictFloat  # noqa
    from pydantic import StrictInt  # noqa
    from pydantic import StrictStr  # noqa
    from pydantic import BaseModel  # noqa
    from pydantic import Field  # noqa
    from pydantic.dataclasses import dataclass as pydantic_dataclass  # noqa

    if PYDANTIC_VERSION == "V1":
        from pydantic.main import ModelMetaclass  # noqa
    else:
        # PYDANTIC_VERSION == "V2"
        from pydantic._internal._model_construction import ModelMetaclass  # noqa

    @pydantic_dataclass
    class Pydantic:
        str_param: str
        int_param: int
        float_param: float
        str_array_param: list[str]
        num_array_param: list[int]
        bool_param: bool
        date_param: datetime
        optional_int_param: int | None = None
        # noinspection PyDataclass
        optional_list_param: list[str] | None = Field(default_factory=list)

    class Basemodel(BaseModel):
        str_param: str
        int_param: int
        float_param: float
        str_array_param: list[str]
        num_array_param: list[int]
        bool_param: bool
        date_param: datetime
        optional_int_param: int | None = None
        # noinspection PyDataclass
        optional_list_param: list[str] | None = Field(default_factory=list)

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

    pydantic = Pydantic(
        str_param="A",
        int_param=1,
        float_param=1.1,
        str_array_param=["A", "B"],
        num_array_param=[1, 2],
        bool_param=False,
        date_param=datetime.strptime("2010-03-25T14:08:00", "%Y-%m-%dT%H:%M:%S"),
    )

    basemodel = Basemodel(
        str_param="A",
        int_param=1,
        float_param=1.1,
        str_array_param=["A", "B"],
        num_array_param=[1, 2],
        bool_param=False,
        date_param=datetime.strptime("2010-03-25T14:08:00", "%Y-%m-%dT%H:%M:%S"),
    )


def params_get_type() -> list[pytest.param]:
    """
    test_type, expected_result
    Used by `test_get_type`
    """
    params = [
        pytest.param(type, type, id="type"),
        pytest.param(object, object, id="object"),
        pytest.param(object(), object, id="object_instance"),
        pytest.param(None, NoneType, id="None"),
        pytest.param(NoneType, NoneType, id="NoneType"),
        pytest.param(int, int, id="int"),
        pytest.param(42, int, id="int_instance"),
        pytest.param(Builtin, Builtin, id="builtin_definition"),
        pytest.param(builtin, Builtin, id="builtin_instance"),
        pytest.param(BuiltinRef, ForwardRef, id="builtin_forward_ref"),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(Pydantic, Pydantic, id="pydantic_definition"),
                pytest.param(pydantic, Pydantic, id="pydantic_instance"),
                pytest.param(PydanticRef, ForwardRef, id="pydantic_forward_ref"),
                pytest.param(BaseModel, BaseModel, id="the_basemodel"),
                pytest.param(Basemodel, Basemodel, id="basemodel_definition"),
                pytest.param(basemodel, Basemodel, id="basemodel_instance"),
                pytest.param(BasemodelRef, ForwardRef, id="basemodel_forward_ref"),
            ]
        )
    return params


@pytest.mark.parametrize("test_type, expected_result", params_get_type())
def test_get_type(test_type: type, expected_result: Any):
    assert get_type(test_type) == expected_result


@pytest.mark.parametrize(
    "test_case",
    [
        pytest.param("fixed_str", id="fixed_str"),
        pytest.param(uuid4().hex[:6], id="random_str"),
    ],
)
def test_builtin_dc_name(test_case: str):
    """Basic functionality check"""
    result = builtin_dc_name(test_case)
    assert isinstance(result, str)
    # these are implementation specific and could change
    assert test_case in result
    assert result.startswith("DataclassFor")


def params_builtin_dc_name_invalid() -> list[pytest.param]:
    """
    test_case
    Used by `test_builtin_dc_name_invalid`
    """
    params = [
        pytest.param(None, id="none"),
        pytest.param(NoneType, id="NoneType"),
        pytest.param(int, id="int_type"),
        pytest.param(42, id="int_instance"),
        pytest.param(BuiltinRef, id="builtin_forward_ref"),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(PydanticRef, id="pydantic_forward_ref"),
                pytest.param(BasemodelRef, id="basemodel_forward_ref"),
            ]
        )
    return params


@pytest.mark.parametrize("test_case", params_builtin_dc_name_invalid())
def test_builtin_dc_name_invalid(test_case: str):
    """Raise an exception if input is not a str"""
    with pytest.raises(RuntimeError):
        builtin_dc_name(test_case)


def params_is_basemodel() -> list[pytest.param]:
    """
    test_type, expected_result
    Used by `test_is_basemodel`
    """
    params = [
        pytest.param(type, False, id="type"),
        pytest.param(object, False, id="object"),
        pytest.param(object(), False, id="object_instance"),
        pytest.param(None, False, id="None"),
        pytest.param(NoneType, False, id="NoneType"),
        pytest.param(int, False, id="int"),
        pytest.param(42, False, id="int_instance"),
        pytest.param(Builtin, False, id="builtin_definition"),
        pytest.param(builtin, False, id="builtin_instance"),
        pytest.param(BuiltinRef, False, id="builtin_forward_ref"),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(Pydantic, False, id="pydantic_definition"),
                pytest.param(pydantic, False, id="pydantic_instance"),
                pytest.param(PydanticRef, False, id="pydantic_forward_ref"),
                pytest.param(Basemodel, True, id="basemodel_definition"),
                pytest.param(basemodel, True, id="basemodel_instance"),
                pytest.param(BasemodelRef, False, id="basemodel_forward_ref"),
            ]
        )
    return params


@pytest.mark.parametrize("test_type, expected_result", params_is_basemodel())
def test_is_basemodel(test_type: type, expected_result: Any):
    """Properly identify BaseModel definitions and instances"""
    assert is_basemodel(test_type) == expected_result


def params_to_builtin_dc_self() -> list[pytest.param]:
    """
    test_type, expected_result
    Used by `test_to_builtin_dc_self`
    """
    params = [
        pytest.param(Builtin, Builtin, id="builtin_definition"),
        pytest.param(builtin, builtin, id="builtin_instance"),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(Pydantic, Pydantic, id="pydantic_definition"),
                pytest.param(pydantic, pydantic, id="pydantic_instance"),
            ]
        )
    return params


@pytest.mark.parametrize("test_type, expected_result", params_to_builtin_dc_self())
def test_to_builtin_dc_self(test_type: type, expected_result: Any):
    """Verify response is self"""
    actual_result = to_builtin_dc(test_type)
    assert actual_result == expected_result
    assert actual_result is expected_result


def params_to_builtin_dc_transform() -> list[pytest.param]:
    """
    test_type, expected_result
    Used by `test_to_builtin_dc_transform`
    """
    params = []
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(Basemodel, Basemodel, id="basemodel_definition"),
                pytest.param(basemodel, basemodel, id="basemodel_instance"),
            ]
        )
    return params


@pytest.mark.parametrize("test_type, expected_result", params_to_builtin_dc_transform())
def test_to_builtin_dc_transform(test_type: type, expected_result: Any):
    """Verify transformed to an annotated (builtin) dataclass"""
    assert not is_dataclass(test_type)
    actual_result = to_builtin_dc(test_type)
    assert is_dataclass(actual_result)
    assert_fields_match(actual_result, expected_result)


def params_to_builtin_dc_copy() -> list[pytest.param]:
    """
    test_type, expected_result
    Used by `test_to_builtin_dc_copy`
    """
    params = [
        pytest.param(Builtin, Builtin, id="builtin_definition"),
        pytest.param(builtin, builtin, id="builtin_instance"),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(Pydantic, Pydantic, id="pydantic_definition"),
                pytest.param(pydantic, pydantic, id="pydantic_instance"),
            ]
        )
    return params


@pytest.mark.parametrize("test_type, expected_result", params_to_builtin_dc_copy())
def test_to_builtin_dc_copy(test_type: type, expected_result: Any):
    """Verify copied to a different annotated (builtin) dataclass"""
    assert is_dataclass(test_type)
    actual_result = to_builtin_dc(test_type, copy_builtin_instance=True)
    assert is_dataclass(actual_result)
    if isinstance(expected_result, type):
        # definition - same type
        assert actual_result is expected_result
    else:
        # instance
        # equality,
        assert actual_result == expected_result
        # but a different instance
        assert actual_result is not expected_result


def params_to_builtin_dc_invalid() -> list[pytest.param]:
    """
    test_type, expected_exception_type
    Used by `test_to_builtin_dc_invalid`
    """
    params = [
        pytest.param(type, ValueError, id="type"),
        pytest.param(object, ValueError, id="object"),
        pytest.param(object(), ValueError, id="object_instance"),
        pytest.param(None, ValueError, id="None"),
        pytest.param(NoneType, ValueError, id="NoneType"),
        pytest.param(int, ValueError, id="int"),
        pytest.param(42, ValueError, id="int_instance"),
        pytest.param(BuiltinRef, ValueError, id="builtin_forward_ref"),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(PydanticRef, ValueError, id="pydantic_forward_ref"),
                pytest.param(BasemodelRef, ValueError, id="pydantic_forward_ref"),
            ]
        )
    return params


@pytest.mark.parametrize("test_type, expected_exception_type", params_to_builtin_dc_invalid())
def test_to_builtin_dc_invalid(test_type: type, expected_exception_type: type[Exception]):
    """Raise an exception if the input is not an annotated (builtin or pydantic) dataclass or BaseModel"""
    with pytest.raises(expected_exception_type):
        to_builtin_dc(test_type)
