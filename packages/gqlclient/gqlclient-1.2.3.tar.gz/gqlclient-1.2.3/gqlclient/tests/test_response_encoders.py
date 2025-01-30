"""
Tests for the response_encoders library
"""
from dataclasses import dataclass

import pytest

from gqlclient import dataclass_encoder
from gqlclient import dict_encoder
from gqlclient import json_encoder
from gqlclient.exceptions import EncoderResponseException
from gqlclient.pydantic_version_util import PYDANTIC_LOADED


@dataclass
class BuiltinChildResponseModel:
    s: str
    i: int


@dataclass
class BuiltinParentResponseModel:
    a: str
    c: BuiltinChildResponseModel


@dataclass
class MutationResponseModel:
    mutation_response: BuiltinParentResponseModel


if PYDANTIC_LOADED:
    from pydantic.dataclasses import dataclass as pydantic_dataclass  # noqa
    from pydantic import BaseModel  # noqa

    @pydantic_dataclass
    class PydanticChildResponseModel:
        s: str
        i: int

    @pydantic_dataclass
    class PydanticParentResponseModel:
        a: str
        c: PydanticChildResponseModel

    class BasemodelChildResponseModel(BaseModel):
        s: str
        i: int

    class BasemodelParentResponseModel(BaseModel):
        a: str
        c: BasemodelChildResponseModel


def params_dataclass_encoder() -> list[pytest.param]:
    """
    call_base, response, response_cls, expected_response_cls_instance
    Used by `test_dataclass_encoder`
    """
    params = [
        (  # dataclass query response without a list
            "call",
            {"call": {"a": "foo", "c": {"s": "bar", "i": 1}}},
            BuiltinParentResponseModel,
            BuiltinParentResponseModel(a="foo", c=BuiltinChildResponseModel(s="bar", i=1)),
        ),
        (  # dataclass query response with a list
            "call",
            {
                "call": [
                    {"a": "foo1", "c": {"s": "bar1", "i": 1}},
                    {"a": "foo2", "c": {"s": "bar2", "i": 2}},
                ]
            },
            BuiltinParentResponseModel,
            [
                BuiltinParentResponseModel(a="foo1", c=BuiltinChildResponseModel(s="bar1", i=1)),
                BuiltinParentResponseModel(a="foo2", c=BuiltinChildResponseModel(s="bar2", i=2)),
            ],
        ),
        (  # dataclass mutation response without a list
            "call",
            {"call": {"mutation_response": {"a": "foo", "c": {"s": "bar", "i": 1}}}},
            MutationResponseModel,
            MutationResponseModel(
                mutation_response=BuiltinParentResponseModel(
                    a="foo", c=BuiltinChildResponseModel(s="bar", i=1)
                )
            ),
        ),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                (  # pydantic dataclass query response without a list
                    "call",
                    {"call": {"a": "foo", "c": {"s": "bar", "i": 1}}},
                    PydanticParentResponseModel,
                    PydanticParentResponseModel(
                        a="foo", c=PydanticChildResponseModel(s="bar", i=1)
                    ),
                ),
                (  # pydantic dataclass query response with a list
                    "call",
                    {
                        "call": [
                            {"a": "foo1", "c": {"s": "bar1", "i": 1}},
                            {"a": "foo2", "c": {"s": "bar2", "i": 2}},
                        ]
                    },
                    PydanticParentResponseModel,
                    [
                        PydanticParentResponseModel(
                            a="foo1", c=PydanticChildResponseModel(s="bar1", i=1)
                        ),
                        PydanticParentResponseModel(
                            a="foo2", c=PydanticChildResponseModel(s="bar2", i=2)
                        ),
                    ],
                ),
                (  # basemodel query response without a list
                    "call",
                    {"call": {"a": "foo", "c": {"s": "bar", "i": 1}}},
                    BasemodelParentResponseModel,
                    BasemodelParentResponseModel(
                        a="foo", c=BasemodelChildResponseModel(s="bar", i=1)
                    ),
                ),
                (  # basemodel query response with a list
                    "call",
                    {
                        "call": [
                            {"a": "foo1", "c": {"s": "bar1", "i": 1}},
                            {"a": "foo2", "c": {"s": "bar2", "i": 2}},
                        ]
                    },
                    BasemodelParentResponseModel,
                    [
                        BasemodelParentResponseModel(
                            a="foo1", c=BasemodelChildResponseModel(s="bar1", i=1)
                        ),
                        BasemodelParentResponseModel(
                            a="foo2", c=BasemodelChildResponseModel(s="bar2", i=2)
                        ),
                    ],
                ),
            ]
        )
    return params


@pytest.mark.parametrize(
    "call_base, response, response_cls, expected_response_cls_instance", params_dataclass_encoder()
)
def test_dataclass_encoder(
    call_base: str, response: dict, response_cls: type, expected_response_cls_instance: object
) -> None:
    assert dataclass_encoder(call_base, response, response_cls) == expected_response_cls_instance


def params_json_encoder() -> list[pytest.param]:
    """
    call_base, response, response_cls, expected_response_cls_instance
    Used by `test_json_encoder`
    """
    params = [
        (  # response without a list
            "foo",
            {"call": {"a": "foo", "c": {"s": "bar", "i": 1}}},
            BuiltinParentResponseModel,
            '{"call": {"a": "foo", "c": {"s": "bar", "i": 1}}}',
        ),
        (  # response with a list
            "foo",
            {
                "call": [
                    {"a": "foo1", "c": {"s": "bar1", "i": 1}},
                    {"a": "foo2", "c": {"s": "bar2", "i": 2}},
                ]
            },
            BuiltinParentResponseModel,
            '{"call": [{"a": "foo1", "c": {"s": "bar1", "i": 1}}, {"a": "foo2", "c": {"s": "bar2", "i": 2}}]}',
        ),
    ]
    return params


@pytest.mark.parametrize(
    "call_base, response, response_cls, expected_response_cls_instance", params_json_encoder()
)
def test_json_encoder(
    call_base: str, response: dict, response_cls: type, expected_response_cls_instance: object
) -> None:
    assert json_encoder(call_base, response, response_cls) == expected_response_cls_instance


def params_dict_encoder() -> list[pytest.param]:
    """
    call_base, response, response_cls, expected_response_cls_instance
    Used by `test_dict_encoder`
    """
    params = [
        (  # response without a list
            "foo",
            {"call": {"a": "foo", "c": {"s": "bar", "i": 1}}},
            BuiltinParentResponseModel,
            {"call": {"a": "foo", "c": {"s": "bar", "i": 1}}},
        ),
        (  # response with a list
            "foo",
            {
                "call": [
                    {"a": "foo1", "c": {"s": "bar1", "i": 1}},
                    {"a": "foo2", "c": {"s": "bar2", "i": 2}},
                ]
            },
            BuiltinParentResponseModel,
            {
                "call": [
                    {"a": "foo1", "c": {"s": "bar1", "i": 1}},
                    {"a": "foo2", "c": {"s": "bar2", "i": 2}},
                ]
            },
        ),
    ]
    return params


@pytest.mark.parametrize(
    "call_base, response, response_cls, expected_response_cls_instance", params_dict_encoder()
)
def test_dict_encoder(
    call_base: str, response: dict, response_cls: type, expected_response_cls_instance: object
) -> None:
    assert dict_encoder(call_base, response, response_cls) == expected_response_cls_instance


def params_encoder_exceptions() -> list[pytest.param]:
    """
    encoder, call_base, response, response_cls
    Used by `test_encoder_exceptions`
    """
    params = [
        pytest.param(dict_encoder, "test", "not a dict", None, id="dict_encoder"),
        pytest.param(json_encoder, "test", object, None, id="json_encoder"),
        pytest.param(
            dataclass_encoder,
            "test",
            {"test": {"bad_attr": 1}},
            BuiltinChildResponseModel,
            id="dataclass_encoder_builtin",
        ),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(
                    dataclass_encoder,
                    "test",
                    {"test": {"bad_attr": 1}},
                    PydanticChildResponseModel,
                    id="dataclass_encoder_pydantic",
                ),
                pytest.param(
                    dataclass_encoder,
                    "test",
                    {"test": {"bad_attr": 1}},
                    BasemodelChildResponseModel,
                    id="dataclass_encoder_basemodel",
                ),
            ]
        )
    return params


@pytest.mark.parametrize("encoder, call_base, response, response_cls", params_encoder_exceptions())
def test_encoder_exceptions(encoder, call_base, response, response_cls):
    """
    Test bad responses to the parametrized encoder raises a EncoderResponseException
    """
    with pytest.raises(EncoderResponseException):
        result = encoder(call_base, response, response_cls)
