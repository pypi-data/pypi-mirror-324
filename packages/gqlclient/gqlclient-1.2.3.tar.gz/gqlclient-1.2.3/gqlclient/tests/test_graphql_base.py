"""
Tests for the graphql_client library
"""
from dataclasses import dataclass
from datetime import datetime

import pytest

from gqlclient import GraphQLClient
from gqlclient.base import dynamic_mutation_param_wrapper
from gqlclient.base import dynamic_query_param_wrapper
from gqlclient.exceptions import ModelException
from gqlclient.pydantic_version_util import PYDANTIC_LOADED
from gqlclient.pydantic_version_util import PYDANTIC_NOT_LOADED
from gqlclient.request_wrap import AbstractWrap
from gqlclient.request_wrap import DynamicWrap
from gqlclient.request_wrap import StaticWrap

QUERY_BASE = "query_base"
MUTATION_BASE = "mutation_base"


# test data based on builtin dataclass
@dataclass
class BuiltinRequest:
    str_param: str
    int_param: int
    float_param: float
    str_array_param: list[str]
    num_array_param: list[int]
    bool_param: bool
    date_param: datetime
    optional_param: int = None


@dataclass
class StaticNestedBuiltinRequest(StaticWrap):
    request_params: BuiltinRequest
    param_name: str = "testParams"


@dataclass
class DynamicNestedBuiltinRequest(DynamicWrap):
    request_params: BuiltinRequest


@dataclass
class BuiltinResponseChild:
    child_param_1: str
    child_param_2: str


@dataclass
class BuiltinResponseParent:
    parent_param_1: str
    parent_param_2: str
    child_object: BuiltinResponseChild


@dataclass
class BuiltinResponseParentWithList:
    parent_param_1: str
    parent_param_2: str
    child_object: list[BuiltinResponseChild]


class BadBuiltin:
    def __init__(self):
        self.str_param = ("A",)
        self.int_param = (1,)
        self.float_param = (1.1,)
        self.str_array_param = (["A", "B"],)
        self.num_array_param = ([1, 2],)
        self.date_param = datetime.strptime("2010-03-25T14:08:00", "%Y-%m-%dT%H:%M:%S")


bad_builtin = BadBuiltin()

builtin_request = BuiltinRequest(
    str_param="A",
    int_param=1,
    float_param=1.1,
    str_array_param=["A", "B"],
    num_array_param=[1, 2],
    bool_param=False,
    date_param=datetime.strptime("2010-03-25T14:08:00", "%Y-%m-%dT%H:%M:%S"),
)

# static param_name from builtin definition
static_nested_builtin_request = StaticNestedBuiltinRequest(
    request_params=builtin_request,
)

dynamic_nested_builtin_request = DynamicNestedBuiltinRequest(
    request_params=builtin_request,
)


if PYDANTIC_LOADED:
    from pydantic.dataclasses import dataclass as pydantic_dataclass  # noqa
    from pydantic import BaseModel  # noqa

    @pydantic_dataclass
    class PydanticRequest:
        str_param: str
        int_param: int
        float_param: float
        str_array_param: list[str]
        num_array_param: list[int]
        bool_param: bool
        date_param: datetime
        optional_param: int = None

    class BasemodelRequest(BaseModel):
        str_param: str
        int_param: int
        float_param: float
        str_array_param: list[str]
        num_array_param: list[int]
        bool_param: bool
        date_param: datetime
        optional_param: int = None

    @dataclass
    class StaticNestedPydanticRequest(StaticWrap):
        request_params: PydanticRequest
        param_name: str = "testParams"

    @dataclass
    class DynamicNestedPydanticRequest(DynamicWrap):
        request_params: PydanticRequest

    @dataclass
    class StaticNestedBasemodelRequest(StaticWrap):
        request_params: BasemodelRequest
        param_name: str = "testParams"

    @dataclass
    class DynamicNestedBasemodelRequest(DynamicWrap):
        request_params: BasemodelRequest

    @pydantic_dataclass
    class PydanticResponseChild:
        child_param_1: str
        child_param_2: str

    @pydantic_dataclass
    class PydanticResponseParent:
        parent_param_1: str
        parent_param_2: str
        child_object: PydanticResponseChild

    class BasemodelResponseParent(BaseModel):
        parent_param_1: str
        parent_param_2: str
        child_object: PydanticResponseChild

    pydantic_request = PydanticRequest(
        str_param="A",
        int_param=1,
        float_param=1.1,
        str_array_param=["A", "B"],
        num_array_param=[1, 2],
        bool_param=False,
        date_param=datetime.strptime("2010-03-25T14:08:00", "%Y-%m-%dT%H:%M:%S"),
    )

    basemodel_request = BasemodelRequest(
        str_param="A",
        int_param=1,
        float_param=1.1,
        str_array_param=["A", "B"],
        num_array_param=[1, 2],
        bool_param=False,
        date_param=datetime.strptime("2010-03-25T14:08:00", "%Y-%m-%dT%H:%M:%S"),
    )

    # static param_name from pydantic definition
    static_nested_pydantic_request = StaticNestedPydanticRequest(
        request_params=pydantic_request,
    )

    dynamic_nested_pydantic_request = DynamicNestedPydanticRequest(
        request_params=pydantic_request,
    )

    # static param_name from basemodel definition
    static_nested_basemodel_request = StaticNestedBasemodelRequest(
        request_params=basemodel_request,
    )

    dynamic_nested_basemodel_request = DynamicNestedBasemodelRequest(
        request_params=basemodel_request,
    )


# Graphql Client to test
@pytest.fixture(scope="module")
def client() -> GraphQLClient:
    return GraphQLClient(gql_uri="http://localhost:5000/graphql")


def params_query_passthrough_with_parameters() -> list[pytest.param]:
    """
    query_base, request_params, response_cls
    Used by `test_query_passthrough_with_parameters`
    """
    params = [
        pytest.param(QUERY_BASE, builtin_request, BuiltinResponseParent, id="builtin_instance"),
        pytest.param(
            QUERY_BASE,
            builtin_request,
            BuiltinResponseParentWithList,
            id="builtin_instance_with_list",
        ),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(
                    QUERY_BASE, pydantic_request, PydanticResponseParent, id="pydantic_instance"
                ),
                pytest.param(
                    QUERY_BASE, basemodel_request, BasemodelResponseParent, id="basemodel_instance"
                ),
            ]
        )
    return params


@pytest.mark.parametrize(
    "query_base, request_params, response_cls", params_query_passthrough_with_parameters()
)
def test_query_passthrough_with_parameters(client, query_base: str, request_params, response_cls):
    """
    Test of query string structure when request params are included for passthrough
    :param client: Graphql Client instance
    :param query_base: Name of the query endpoint
    :param request_params: Instance of a simple dataclass containing the request parameters
    :param response_cls: Dataclass containing the attributes of the graphql response
    :return: None
    """
    assert not isinstance(
        request_params, AbstractWrap
    ), "Invalid test fixture. Cannot be AbstractWrap for this test."

    test_query = client.get_query(
        query_base=query_base, query_parameters=request_params, query_response_cls=response_cls
    )
    assert "query" in test_query
    expected_query_str = (
        "{query_base("
        'str_param: "A", '
        "int_param: 1, "
        "float_param: 1.1, "
        'str_array_param: ["A", "B"], '
        "num_array_param: [1, 2], "
        "bool_param: false, "
        'date_param: "2010-03-25T14:08:00")'
        "{parent_param_1, parent_param_2, "
        "child_object { child_param_1 child_param_2 }"
        "} }"
    )
    assert test_query["query"] == expected_query_str


def params_query_static_nest_with_parameters() -> list[pytest.param]:
    """
    query_base, request_object, response_cls
    Used by `test_query_static_nest_with_parameters`
    """
    params = [
        pytest.param(
            QUERY_BASE,
            static_nested_builtin_request,
            BuiltinResponseParent,
            id="builtin_static_request",
        ),
        pytest.param(
            QUERY_BASE,
            static_nested_builtin_request,
            BuiltinResponseParentWithList,
            id="builtin_static_request_with_list",
        ),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(
                    QUERY_BASE,
                    static_nested_pydantic_request,
                    PydanticResponseParent,
                    id="pydantic_static_request",
                ),
                pytest.param(
                    QUERY_BASE,
                    static_nested_basemodel_request,
                    BasemodelResponseParent,
                    id="basemodel_static_request",
                ),
            ]
        )
    return params


@pytest.mark.parametrize(
    "query_base, request_object, response_cls", params_query_static_nest_with_parameters()
)
def test_query_static_nest_with_parameters(client, query_base: str, request_object, response_cls):
    """
    Test of query string structure when request params and `param_name` are included
    :param client: Graphql Client instance
    :param query_base: Name of the query endpoint
    :param request_object: Instance of a StaticWrap dataclass containing the `request_params` and static `param_name`
    :param response_cls: Dataclass containing the attributes of the graphql response
    :return: None
    """
    assert isinstance(
        request_object, StaticWrap
    ), "Invalid test fixture. StaticWrap required for this test."

    test_query = client.get_query(
        query_base=query_base, query_parameters=request_object, query_response_cls=response_cls
    )
    param_wrapper = request_object.param_name
    assert "query" in test_query
    expected_query_str = (
        "{query_base("
        f"{param_wrapper}: "
        '{str_param: "A", '
        "int_param: 1, "
        "float_param: 1.1, "
        'str_array_param: ["A", "B"], '
        "num_array_param: [1, 2], "
        "bool_param: false, "
        'date_param: "2010-03-25T14:08:00"})'
        "{parent_param_1, parent_param_2, "
        "child_object { child_param_1 child_param_2 }"
        "} }"
    )
    assert test_query["query"] == expected_query_str


def params_query_dynamic_nest_with_parameters() -> list[pytest.param]:
    """
    query_base, request_object, response_cls
    Used by `test_query_dynamic_nest_with_parameters`
    """
    params = [
        pytest.param(
            QUERY_BASE,
            dynamic_nested_builtin_request,
            BuiltinResponseParent,
            id="builtin_dynamic_request",
        ),
        pytest.param(
            QUERY_BASE,
            dynamic_nested_builtin_request,
            BuiltinResponseParentWithList,
            id="builtin_dynamic_request_with_list",
        ),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(
                    QUERY_BASE,
                    dynamic_nested_pydantic_request,
                    PydanticResponseParent,
                    id="builtin_pydantic_request",
                ),
                pytest.param(
                    QUERY_BASE,
                    dynamic_nested_basemodel_request,
                    BasemodelResponseParent,
                    id="builtin_basemodel_request",
                ),
            ]
        )
    return params


@pytest.mark.parametrize(
    "query_base, request_object, response_cls", params_query_dynamic_nest_with_parameters()
)
def test_query_dynamic_nest_with_parameters(
    client,
    query_base: str,
    request_object: object,
    response_cls: type,
):
    """
    Test of query string structure when request params are included and `param_name` will be determined dynamically
    :param client: Graphql Client instance
    :param query_base: Name of the query endpoint
    :param request_object: Instance of a DynamicWrap dataclass containing the `request_params`
    :param response_cls: Dataclass containing the attributes of the graphql response
    :return: None
    """
    assert isinstance(
        request_object, DynamicWrap
    ), "Invalid test fixture. DynamicWrap required for this test."

    test_query = client.get_query(
        query_base=query_base, query_parameters=request_object, query_response_cls=response_cls
    )
    param_wrapper = dynamic_query_param_wrapper()
    assert "query" in test_query
    expected_query_str = (
        "{query_base("
        f"{param_wrapper}: "
        '{str_param: "A", '
        "int_param: 1, "
        "float_param: 1.1, "
        'str_array_param: ["A", "B"], '
        "num_array_param: [1, 2], "
        "bool_param: false, "
        'date_param: "2010-03-25T14:08:00"})'
        "{parent_param_1, parent_param_2, "
        "child_object { child_param_1 child_param_2 }"
        "} }"
    )
    assert test_query["query"] == expected_query_str


def params_query_without_parameters() -> list[pytest.param]:
    """
    query_base, response_cls
    Used by `test_query_without_parameters`
    """
    params = [
        pytest.param(QUERY_BASE, BuiltinResponseParent, id="builtin_response"),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(QUERY_BASE, PydanticResponseParent, id="pydantic_response"),
                pytest.param(QUERY_BASE, BasemodelResponseParent, id="basemodel_response"),
            ]
        )
    return params


@pytest.mark.parametrize("query_base, response_cls", params_query_without_parameters())
def test_query_without_parameters(client, query_base: str, response_cls):
    """
    Test of query string structure when parameter model is NOT included
    :param client: Graphql Client instance
    :param query_base: Name of the query endpoint
    :param response_cls: Dataclass containing the attributes of the graphql response
    :return: None
    """
    test_query = client.get_query(query_base=query_base, query_response_cls=response_cls)
    assert "query" in test_query
    expected_query_str = (
        "{query_base"
        "{parent_param_1, parent_param_2, "
        "child_object { child_param_1 child_param_2 }"
        "} }"
    )

    assert test_query["query"] == expected_query_str


def params_mutation_passthrough_with_response() -> list[pytest.param]:
    """
    mutation_base, request_params, response_cls
    Used by `test_mutation_passthrough_with_response`
    """
    params = [
        pytest.param(MUTATION_BASE, builtin_request, BuiltinResponseParent, id="builtin"),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(
                    MUTATION_BASE, pydantic_request, PydanticResponseParent, id="pydantic"
                ),
                pytest.param(
                    MUTATION_BASE, basemodel_request, BasemodelResponseParent, id="basemodel"
                ),
            ]
        )
    return params


@pytest.mark.parametrize(
    "mutation_base, request_params, response_cls", params_mutation_passthrough_with_response()
)
def test_mutation_passthrough_with_response(
    client, mutation_base: str, request_params, response_cls
):
    """
    Test of mutation string structure when response model is included and request params are included for passthrough
    :param client: Graphql Client instance
    :param mutation_base: Name of the mutation endpoint
    :param request_params: Instance of a simple dataclass containing the request parameters
    :param response_cls: Dataclass containing the attributes of the graphql response
    :return: None
    """
    assert not isinstance(
        request_params, AbstractWrap
    ), "Invalid test fixture. Cannot be AbstractWrap for this test."

    test_mutation = client.get_mutation(
        mutation_base=mutation_base,
        mutation_response_cls=response_cls,
        mutation_parameters=request_params,
    )
    assert "query" in test_mutation
    assert "operationName" in test_mutation
    expected_query_str = (
        "mutation mutation_base "
        "{mutation_base("
        'str_param: "A", '
        "int_param: 1, "
        "float_param: 1.1, "
        'str_array_param: ["A", "B"], '
        "num_array_param: [1, 2], "
        "bool_param: false, "
        'date_param: "2010-03-25T14:08:00")'
        "{parent_param_1, parent_param_2, child_object "
        "{ child_param_1 child_param_2 }} }"
    )

    assert test_mutation["query"] == expected_query_str
    assert test_mutation["operationName"] == "mutation_base"


def params_mutation_static_nest_with_response() -> list[pytest.param]:
    """
    mutation_base, request_object, response_cls
    Used by `test_mutation_static_nest_with_response`
    """
    params = [
        pytest.param(
            MUTATION_BASE,
            static_nested_builtin_request,
            BuiltinResponseParent,
            id="builtin_static_request",
        ),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(
                    MUTATION_BASE,
                    static_nested_pydantic_request,
                    PydanticResponseParent,
                    id="pydantic_static_request",
                ),
                pytest.param(
                    MUTATION_BASE,
                    static_nested_basemodel_request,
                    BasemodelResponseParent,
                    id="basemodel_static_request",
                ),
            ]
        )
    return params


@pytest.mark.parametrize(
    "mutation_base, request_object, response_cls", params_mutation_static_nest_with_response()
)
def test_mutation_static_nest_with_response(
    client, mutation_base: str, request_object, response_cls
):
    """
    Test of mutation string structure when response model is included and request params and `param_name` are included
    :param client: Graphql Client instance
    :param mutation_base: Name of the mutation endpoint
    :param request_object: Instance of a StaticWrap dataclass containing the `request_params` and static `param_name`
    :param response_cls: Dataclass containing the attributes of the graphql response
    :return: None
    """
    assert isinstance(
        request_object, StaticWrap
    ), "Invalid test fixture. StaticWrap required for this test."

    test_mutation = client.get_mutation(
        mutation_base=mutation_base,
        mutation_response_cls=response_cls,
        mutation_parameters=request_object,
    )
    param_wrapper = request_object.param_name  # noqa
    assert "query" in test_mutation
    assert "operationName" in test_mutation
    expected_query_str = (
        "mutation mutation_base "
        "{mutation_base("
        f"{param_wrapper}: "
        '{str_param: "A", '
        "int_param: 1, "
        "float_param: 1.1, "
        'str_array_param: ["A", "B"], '
        "num_array_param: [1, 2], "
        "bool_param: false, "
        'date_param: "2010-03-25T14:08:00"})'
        "{parent_param_1, parent_param_2, child_object "
        "{ child_param_1 child_param_2 }} }"
    )

    assert test_mutation["query"] == expected_query_str
    assert test_mutation["operationName"] == "mutation_base"


def params_mutation_dynamic_nest_with_response() -> list[pytest.param]:
    """
    mutation_base, request_object, response_cls
    Used by `test_mutation_dynamic_nest_with_response`
    """
    params = [
        pytest.param(
            MUTATION_BASE,
            dynamic_nested_builtin_request,
            BuiltinResponseParent,
            id="builtin_dynamic_request",
        ),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(
                    MUTATION_BASE,
                    dynamic_nested_pydantic_request,
                    PydanticResponseParent,
                    id="pydantic_dynamic_request",
                ),
                pytest.param(
                    MUTATION_BASE,
                    dynamic_nested_basemodel_request,
                    BasemodelResponseParent,
                    id="basemodel_dynamic_request",
                ),
            ]
        )
    return params


@pytest.mark.parametrize(
    "mutation_base, request_object, response_cls", params_mutation_dynamic_nest_with_response()
)
def test_mutation_dynamic_nest_with_response(
    client, mutation_base: str, request_object, response_cls
):
    """
    Test of mutation string structure when response model is included and request params are included
    and `param_name` will be determined dynamically.
    :param client: Graphql Client instance
    :param mutation_base: Name of the mutation endpoint
    :param request_object: Instance of a DynamicWrap dataclass containing the `request_params`
    :param response_cls: Dataclass containing the attributes of the graphql response
    :return: None
    """
    assert isinstance(
        request_object, DynamicWrap
    ), "Invalid test fixture. DynamicWrap required for this test."

    test_mutation = client.get_mutation(
        mutation_base=mutation_base,
        mutation_response_cls=response_cls,
        mutation_parameters=request_object,
    )
    param_wrapper = dynamic_mutation_param_wrapper(mutation_base)
    assert "query" in test_mutation
    assert "operationName" in test_mutation
    expected_query_str = (
        "mutation mutation_base "
        "{mutation_base("
        f"{param_wrapper}: "
        '{str_param: "A", '
        "int_param: 1, "
        "float_param: 1.1, "
        'str_array_param: ["A", "B"], '
        "num_array_param: [1, 2], "
        "bool_param: false, "
        'date_param: "2010-03-25T14:08:00"})'
        "{parent_param_1, parent_param_2, child_object "
        "{ child_param_1 child_param_2 }} }"
    )

    assert test_mutation["query"] == expected_query_str
    assert test_mutation["operationName"] == "mutation_base"


def params_mutation_passthrough_without_response() -> list[pytest.param]:
    """
    mutation_base, request_params
    Used by `test_mutation_passthrough_without_response`
    """
    params = [
        pytest.param(MUTATION_BASE, builtin_request, id="builtin"),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(MUTATION_BASE, pydantic_request, id="pydantic"),
                pytest.param(MUTATION_BASE, basemodel_request, id="basemodel"),
            ]
        )
    return params


@pytest.mark.parametrize(
    "mutation_base, request_params", params_mutation_passthrough_without_response()
)
def test_mutation_passthrough_without_response(client, mutation_base: str, request_params):
    """
    Test of mutation string structure when response model is NOT included
    and request params are included for passthrough
    :param client: Graphql Client instance
    :param mutation_base: Name of the mutation endpoint
    :param request_params: Instance of a simple dataclass containing the request parameters
    :return: None
    """
    assert not isinstance(
        request_params, AbstractWrap
    ), "Invalid test fixture. Cannot be AbstractWrap for this test."

    test_mutation = client.get_mutation(
        mutation_base=mutation_base, mutation_parameters=request_params
    )
    assert "query" in test_mutation
    assert "operationName" in test_mutation
    expected_query_str = (
        "mutation mutation_base "
        "{mutation_base("
        'str_param: "A", '
        "int_param: 1, float_param: 1.1, "
        'str_array_param: ["A", "B"], '
        "num_array_param: [1, 2], "
        "bool_param: false, "
        'date_param: "2010-03-25T14:08:00") }'
    )

    assert test_mutation["query"] == expected_query_str
    assert test_mutation["operationName"] == "mutation_base"


def params_mutation_static_nest_without_response() -> list[pytest.param]:
    """
    mutation_base, request_object
    Used by `test_mutation_static_nest_without_response`
    """
    params = [
        pytest.param(MUTATION_BASE, static_nested_builtin_request, id="builtin"),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(MUTATION_BASE, static_nested_pydantic_request, id="pydantic"),
                pytest.param(MUTATION_BASE, static_nested_basemodel_request, id="basemodel"),
            ]
        )
    return params


@pytest.mark.parametrize(
    "mutation_base, request_object", params_mutation_static_nest_without_response()
)
def test_mutation_static_nest_without_response(client, mutation_base: str, request_object):
    """
    Test of mutation string structure when response model is NOT included
    but request params and `param_name` are included
    :param client: Graphql Client instance
    :param mutation_base: Name of the mutation endpoint
    :param request_object: Instance of a StaticWrap dataclass containing the `request_params` and static `param_name`
    :return: None
    """
    assert isinstance(
        request_object, StaticWrap
    ), "Invalid test fixture. StaticWrap required for this test."

    test_mutation = client.get_mutation(
        mutation_base=mutation_base, mutation_parameters=request_object
    )
    param_wrapper = request_object.param_name
    assert "query" in test_mutation
    assert "operationName" in test_mutation
    expected_query_str = (
        "mutation mutation_base "
        "{mutation_base("
        f"{param_wrapper}: "
        '{str_param: "A", '
        "int_param: 1, float_param: 1.1, "
        'str_array_param: ["A", "B"], '
        "num_array_param: [1, 2], "
        "bool_param: false, "
        'date_param: "2010-03-25T14:08:00"}) }'
    )

    assert test_mutation["query"] == expected_query_str
    assert test_mutation["operationName"] == "mutation_base"


def params_mutation_dynamic_nest_without_response() -> list[pytest.param]:
    """
    mutation_base, request_object
    Used by `test_mutation_dynamic_nest_without_response`
    """
    params = [
        pytest.param(MUTATION_BASE, dynamic_nested_builtin_request, id="builtin_dynamic_nested"),
    ]
    if PYDANTIC_LOADED:
        params.extend(
            [
                pytest.param(
                    MUTATION_BASE, dynamic_nested_pydantic_request, id="pydantic_dynamic_nested"
                ),
                pytest.param(
                    MUTATION_BASE, dynamic_nested_basemodel_request, id="basemodel_dynamic_nested"
                ),
            ]
        )
    return params


@pytest.mark.parametrize(
    "mutation_base, request_object", params_mutation_dynamic_nest_without_response()
)
def test_mutation_dynamic_nest_without_response(client, mutation_base: str, request_object):
    """
    Test of mutation string structure when response model is NOT included and request params are included
    and `param_name` will be determined dynamically.
    :param client: Graphql Client instance
    :param mutation_base: Name of the mutation endpoint
    :param request_object: Instance of a DynamicWrap dataclass containing the `request_params`
    :return: None
    """
    assert isinstance(
        request_object, DynamicWrap
    ), "Invalid test fixture. DynamicWrap required for this test."

    test_mutation = client.get_mutation(
        mutation_base=mutation_base, mutation_parameters=request_object
    )
    param_wrapper = dynamic_mutation_param_wrapper(mutation_name=mutation_base)
    assert "query" in test_mutation
    assert "operationName" in test_mutation
    expected_query_str = (
        "mutation mutation_base "
        "{mutation_base("
        f"{param_wrapper}: "
        '{str_param: "A", '
        "int_param: 1, float_param: 1.1, "
        'str_array_param: ["A", "B"], '
        "num_array_param: [1, 2], "
        "bool_param: false, "
        'date_param: "2010-03-25T14:08:00"}) }'
    )

    assert test_mutation["query"] == expected_query_str
    assert test_mutation["operationName"] == "mutation_base"


def params_bad_model() -> list[pytest.param]:
    """
    response_model_cls, parameter_model
    Used by `test_bad_model`
    """
    params = [
        pytest.param(BadBuiltin, None, id="no_params"),
        pytest.param(BuiltinResponseParent, bad_builtin, id="with_params"),
    ]
    return params


@pytest.mark.parametrize("response_model_cls, parameter_model", params_bad_model())
def test_bad_model(client, response_model_cls, parameter_model):
    """
    Test of a non-dataclass object causing a ValueError
    :param client: Graphql Client instance
    :param response_model_cls: Object representing the graphql response
    :param parameter_model: Object representing the graphql parameters
    :return: None
    """

    with pytest.raises(ModelException):
        client.get_query(QUERY_BASE, response_model_cls, parameter_model)


def test_query_with_empty_parameters(client):
    """
    Test query with a parameter object with all None attribute values
    :param client: Graphql Client instance
    :return:
    """

    # noinspection PyTypeChecker
    empty_dataclass_parameters = BuiltinRequest(
        str_param=None,
        int_param=None,
        float_param=None,
        str_array_param=None,
        num_array_param=None,
        bool_param=None,
        date_param=None,
    )

    test_query = client.get_query(
        query_base=QUERY_BASE,
        query_parameters=empty_dataclass_parameters,
        query_response_cls=BuiltinResponseParent,
    )
    assert "query" in test_query
    expected_query_str = (
        "{query_base"
        "{parent_param_1, parent_param_2, "
        "child_object { child_param_1 child_param_2 }"
        "} }"
    )

    assert test_query["query"] == expected_query_str


def test_builtin_three_layered_response(client):
    @dataclass
    class Grandchild:
        grandchild_name: str

    @dataclass
    class Child:
        child_name: str
        grandchild: Grandchild

    @dataclass
    class Parent:
        parent_name: str
        child: Child

    test_query = client.get_query("builtinThreeLayer", Parent)

    expected_query = {
        "query": "{builtinThreeLayer"
        "{parent_name, "
        "child { child_name grandchild { grandchild_name } }"
        "} }"
    }
    assert test_query == expected_query


@pytest.mark.skipif(PYDANTIC_NOT_LOADED, reason="Pydantic not loaded")
def test_pydantic_three_layered_response(client):
    @pydantic_dataclass
    class Grandchild:
        grandchild_name: str

    @pydantic_dataclass
    class Child:
        child_name: str
        grandchild: Grandchild

    @pydantic_dataclass
    class Parent:
        parent_name: str
        child: Child

    test_query = client.get_query("pydanticThreeLayer", Parent)

    expected_query = {
        "query": "{pydanticThreeLayer"
        "{parent_name, "
        "child { child_name grandchild { grandchild_name } }"
        "} }"
    }
    assert test_query == expected_query


@pytest.mark.skipif(PYDANTIC_NOT_LOADED, reason="Pydantic not loaded")
def test_basemodel_three_layered_response(client):
    class Grandchild(BaseModel):
        grandchild_name: str

    class Child(BaseModel):
        child_name: str
        grandchild: Grandchild

    class Parent(BaseModel):
        parent_name: str
        child: Child

    test_query = client.get_query("basemodelThreeLayer", Parent)

    expected_query = {
        "query": "{basemodelThreeLayer"
        "{parent_name, "
        "child { child_name grandchild { grandchild_name } }"
        "} }"
    }
    assert test_query == expected_query
