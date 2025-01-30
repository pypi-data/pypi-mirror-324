from dataclasses import is_dataclass
from dataclasses import MISSING
from typing import Any

from gqlclient.pydantic_utils import get_type
from gqlclient.pydantic_utils import is_basemodel
from gqlclient.pydantic_version_util import PYDANTIC_VERSION

if PYDANTIC_VERSION == "V1":
    pass

elif PYDANTIC_VERSION == "V2":
    from pydantic_core import PydanticUndefined  # noqa


def assert_fields_match(dc: Any, bm: Any):
    """
    Equality check to simplify testing
    """
    assert is_dataclass(dc)
    assert not is_dataclass(bm)
    assert is_basemodel(bm)

    # type checks
    builtin_type = get_type(dc)
    bm_type = get_type(bm)

    # __annotations__
    assert builtin_type.__annotations__ == bm_type.__annotations__

    # noinspection PyUnresolvedReferences
    builtin_fields = builtin_type.__dataclass_fields__

    if hasattr(bm_type, "__pydantic_fields__"):
        # V2
        basemodel_fields = getattr(bm_type, "__pydantic_fields__")
    elif hasattr(bm_type, "__fields__"):
        # V1 - deprecated for V2
        basemodel_fields = getattr(bm_type, "__fields__")
    else:
        message = f"Unexpected outcome - basemodel is missing V1 __fields__ and V2 __pydantic_fields__: {bm_type!r}"
        raise RuntimeError(message)

    assert builtin_fields.keys() == basemodel_fields.keys()

    for field in builtin_fields.values():
        assert basemodel_fields[field.name].annotation == field.type
        if field.default is not MISSING:
            assert basemodel_fields[field.name].default == field.default
        elif field.default_factory is not MISSING:
            assert basemodel_fields[field.name].default_factory == field.default_factory
        else:
            if PYDANTIC_VERSION == "V2":
                assert basemodel_fields[field.name].default is PydanticUndefined
            else:
                assert basemodel_fields[field.name].default is None

    # If it is an instance, also ensure that the values match for each field
    if not isinstance(dc, type) or not isinstance(bm, type):
        for field_name in builtin_fields:
            assert getattr(dc, field_name) == getattr(bm, field_name)
