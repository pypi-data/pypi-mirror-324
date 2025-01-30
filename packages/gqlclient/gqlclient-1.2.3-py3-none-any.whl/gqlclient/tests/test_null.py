"""
Tests for NULL processing
"""
from dataclasses import dataclass
from typing import Any

import pytest

from gqlclient.base import GraphQLClientBase
from gqlclient.null import NULL
from gqlclient.null import NullType
from gqlclient.pydantic_version_util import PYDANTIC_LOADED


@dataclass
class Builtin:
    value: str = "builtin dataclass"
    optInt: int | None = None
    nullableInt: int | NullType = NULL


if PYDANTIC_LOADED:
    from pydantic import ValidationError  # noqa
    from pydantic.dataclasses import dataclass as pydantic_dataclass  # noqa
    from pydantic import BaseModel  # noqa

    @pydantic_dataclass
    class Pydantic:
        value: str = "pydantic"
        optInt: int | None = None
        nullableInt: int | NullType = NULL

    class Basemodel(BaseModel):
        value: str = "basemodel"
        optInt: int | None = None
        nullableInt: int | NullType = NULL


def params_null() -> list[pytest.param]:
    """
    request_params
    Used by `test_null`
    """
    params = [
        pytest.param(Builtin(), id="builtin"),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(Pydantic(), id="pydantic"),
                pytest.param(Basemodel(), id="basemodel"),
            ]
        )
    return params


@pytest.mark.parametrize("request_params", params_null())
def test_null(request_params: object):
    """
    Verify None fields are excluded from the resulting string.
    Verify NULL field gets retained with a value of `null`.
    """
    result_string = GraphQLClientBase._graphql_query_parameters_from_model(model=request_params)
    assert "value" in result_string
    assert "optInt" not in result_string
    assert "nullableInt" in result_string
    for kv_string in result_string.split(","):
        k, v = kv_string.split(":")
        if k.strip() == "nullableInt":
            assert v.strip() == "null"


def params_null_invalid() -> list[pytest.param]:
    """
    request_param
    Used by `test_null_invalid_pydantic` and `test_null_invalid_basemodel`
    """
    params = []
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param({"optInt": "a_string"}, id="opt_with_str"),
                pytest.param({"nullableInt": "a_string"}, id="null_with_str"),
                pytest.param({"optInt": NULL}, id="opt_with_null"),
                pytest.param({"nullableInt": None}, id="null_with_none"),
            ]
        )
    return params


@pytest.mark.parametrize("request_param", params_null_invalid())
def test_null_invalid_pydantic(request_param: dict[str, Any]):
    """
    Verify ValidationError for invalid inputs to Pydantic dataclass.
    """
    with pytest.raises(ValidationError):
        Pydantic(**request_param)


@pytest.mark.parametrize("request_param", params_null_invalid())
def test_null_invalid_basemodel(request_param: dict[str, Any]):
    """
    Verify ValidationError for invalid inputs to BaseModel dataclass.
    """
    with pytest.raises(ValidationError):
        Basemodel(**request_param)
