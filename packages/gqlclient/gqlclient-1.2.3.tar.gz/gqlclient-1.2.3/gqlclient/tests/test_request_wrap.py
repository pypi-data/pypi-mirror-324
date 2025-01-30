"""
Tests for request wrapping
"""
from dataclasses import asdict
from dataclasses import dataclass

import pytest

from gqlclient.pydantic_version_util import PYDANTIC_LOADED
from gqlclient.request_wrap import AbstractWrap
from gqlclient.request_wrap import DynamicWrap
from gqlclient.request_wrap import StaticWrap
from gqlclient.request_wrap import wrap_request


@dataclass
class Builtin:
    value: str = "builtin dataclass"
    optInt: int | None = None


if PYDANTIC_LOADED:
    from pydantic.dataclasses import dataclass as pydantic_dataclass  # noqa
    from pydantic import BaseModel  # noqa

    @pydantic_dataclass
    class Pydantic:
        value: str = "pydantic"
        optInt: int | None = None

    class Basemodel(BaseModel):
        value: str = "basemodel"
        optInt: int | None = None


def params_dataclasses_dynamic() -> list[pytest.param]:
    """
    request_params
    Used by `test_dataclasses_dynamic`
    """
    params = [
        pytest.param(Builtin(), id="builtin"),
        pytest.param(None, id="none"),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(Pydantic(), id="pydantic"),
                pytest.param(Basemodel(), id="basemodel"),
            ]
        )
    return params


@pytest.mark.parametrize("request_params", params_dataclasses_dynamic())
def test_dataclasses_dynamic(request_params):
    """Verify proper dynamic dataclass instantiation"""
    result: DynamicWrap = DynamicWrap(request_params=request_params)
    assert result
    assert isinstance(result, DynamicWrap)
    result_data = asdict(result)
    # verify param_name is excluded from result
    assert "param_name" not in result_data.keys()
    assert "request_params" in result_data.keys()
    if request_params is None:
        assert result.request_params is None
    else:
        assert result.request_params == request_params
        assert result.request_params is request_params


def params_dataclasses_static() -> list[pytest.param]:
    """
    request_params
    Used by `test_dataclasses_static`
    """
    params = [
        pytest.param(Builtin(), id="builtin"),
        pytest.param(None, id="none"),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(Pydantic(), id="pydantic"),
                pytest.param(Basemodel(), id="basemodel"),
            ]
        )
    return params


@pytest.mark.parametrize("request_params", params_dataclasses_static())
def test_dataclasses_static(request_params):
    """Verify proper static dataclass instantiation"""
    result: StaticWrap = StaticWrap(request_params=request_params, param_name="whatever")
    assert result
    assert isinstance(result, StaticWrap)
    result_data = asdict(result)
    # verify param_name is included in result
    assert "param_name" in result_data.keys()
    assert result_data["param_name"] == "whatever"
    assert "request_params" in result_data.keys()
    if request_params is None:
        assert result.request_params is None
    else:
        assert result.request_params == request_params
        assert result.request_params is request_params


def params_dataclasses_abstract() -> list[pytest.param]:
    """
    request_params, expected_exception_type
    Used by `test_dataclasses_abstract`
    """
    params = [
        pytest.param(Builtin(), TypeError, id="builtin"),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(Pydantic(), TypeError, id="pydantic"),
                pytest.param(Basemodel(), TypeError, id="basemodel"),
            ]
        )
    return params


@pytest.mark.parametrize("request_params, expected_exception_type", params_dataclasses_abstract())
def test_dataclasses_abstract(request_params, expected_exception_type: type[Exception]):
    """Verify AbstractWrap cannot be instantiated"""
    with pytest.raises(expected_exception_type):
        AbstractWrap(request_params=request_params)


def params_dataclasses_invalid() -> list[pytest.param]:
    """
    request_params, expected_exception_type
    Used by `test_dataclasses_invalid`
    """
    params = [
        pytest.param("a_string", TypeError, id="string"),
        pytest.param(int, TypeError, id="int"),
        pytest.param({"a_key": "a_value"}, TypeError, id="dict"),
        pytest.param([], TypeError, id="list"),
    ]
    return params


@pytest.mark.parametrize("request_params, expected_exception_type", params_dataclasses_invalid())
def test_dataclasses_invalid(request_params, expected_exception_type: type[Exception]):
    """Verify request params must be a dataclass"""
    with pytest.raises(expected_exception_type):
        DynamicWrap(request_params=request_params)
    with pytest.raises(expected_exception_type):
        StaticWrap(request_params=request_params, param_name="whatever")


def params_wrap_request() -> list[pytest.param]:
    """
    request_params
    Used by `test_wrap_request`
    """
    params = [
        pytest.param(Builtin(), id="builtin_instance"),
        pytest.param(None, id="none"),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(Pydantic(), id="pydantic_instance"),
                pytest.param(Basemodel(), id="basemodel_instance"),
            ]
        )
    return params


@pytest.mark.parametrize("request_params", params_wrap_request())
def test_wrap_request(request_params):
    """Verify proper result from wrap_request"""
    result: DynamicWrap = wrap_request(request_params=request_params)
    assert result
    assert isinstance(result, DynamicWrap)
    result_data = asdict(result)
    # verify param_name is excluded from result
    assert "param_name" not in result_data.keys()
    assert "request_params" in result_data.keys()
    if request_params is None:
        assert result.request_params is None
    else:
        assert result.request_params == request_params
        assert result.request_params is request_params

    result: StaticWrap = wrap_request(request_params=request_params, param_name="whatever")
    assert result
    assert isinstance(result, StaticWrap)
    result_data = asdict(result)
    # verify param_name is included in result
    assert "param_name" in result_data.keys()
    assert result_data["param_name"] == "whatever"
    assert "request_params" in result_data.keys()
    if request_params is None:
        assert result.request_params is None
    else:
        assert result.request_params == request_params
        assert result.request_params is request_params


def params_wrap_request_invalid_inputs() -> list[pytest.param]:
    """
    request_params, expected_exception_type
    Used by `test_wrap_request_invalid_inputs`
    """
    params = [
        pytest.param(Builtin, TypeError, id="builtin_definition"),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(Pydantic, TypeError, id="pydantic_definition"),
                pytest.param(Basemodel, TypeError, id="basemodel_definition"),
            ]
        )
    return params


@pytest.mark.parametrize(
    "request_params, expected_exception_type", params_wrap_request_invalid_inputs()
)
def test_wrap_request_invalid_inputs(request_params, expected_exception_type: type[Exception]):
    """Verify proper result from wrap_request for invalid input"""
    with pytest.raises(expected_exception_type):
        wrap_request(request_params=request_params)
    with pytest.raises(expected_exception_type):
        wrap_request(request_params=request_params, param_name="whatever")
