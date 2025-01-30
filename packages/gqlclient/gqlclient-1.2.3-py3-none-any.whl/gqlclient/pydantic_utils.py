from dataclasses import field as dc_field
from dataclasses import fields as dc_fields
from dataclasses import is_dataclass
from dataclasses import make_dataclass
from typing import Any

from gqlclient.pydantic_version_util import PYDANTIC_NOT_LOADED
from gqlclient.pydantic_version_util import PYDANTIC_VERSION


def get_type(obj) -> type:
    """
    Get the type associated with an object.
    - For an instance, this will be the corresponding class.
    - For a class, this will be the class itself.
    - For a custom metaclass, this will be the custom metaclass itself.
    - For `type` (the default metaclass), this will be `type`.
    """
    # class and metaclass definitions are an instance of `type`, so the provided `obj` IS the class
    # otherwise, get the type of the instance, which will either be a class or metaclass definition
    return obj if isinstance(obj, type) else type(obj)


def builtin_dc_name(basemodel_name: str) -> str:
    """
    Returns the name that gets assigned to the annotated (builtin) dataclass that is created from a BaseModel.
    """
    if not isinstance(basemodel_name, str):
        raise RuntimeError(f"basemodel_name must be a str.  Received: {type(basemodel_name)}")
    return f"DataclassFor{basemodel_name}"


if PYDANTIC_NOT_LOADED:

    def is_basemodel(model: object) -> bool:
        # since pydantic is not loaded, this cannot be True
        return False

    def to_builtin_dc(
        bm: Any,
        *,
        copy_builtin_instance: bool = False,
    ) -> type:
        """
        This will get called if no pydantic libraries are installed.
        This means the only possible dataclass form is a builtin dataclass.
        """

        # prep and handle exception cases
        is_type = isinstance(bm, type)
        is_instance = not is_type
        tp = get_type(bm)

        if not is_dataclass(tp):
            if is_type:
                message = f"Type {bm.__name__!r} is not a builtin dataclass."
            else:
                message = f"Instance of {type(bm).__name__!r} is not a builtin dataclass: {bm!r}"
            raise ValueError(message)

        if is_instance:
            if copy_builtin_instance:
                # return a shallow copy of the annotated dataclass instance
                data = {field.name: getattr(bm, field.name) for field in dc_fields(bm)}
                return tp(**data)
            # return the same annotated dataclass instance
            return bm
        else:
            # return the provided annotated dataclass definition
            return tp

elif PYDANTIC_VERSION == "V1":

    from pydantic.main import ModelMetaclass  # noqa

    def is_basemodel(model: object) -> bool:
        return isinstance(get_type(model), ModelMetaclass)

    def to_builtin_dc(
        bm: Any,
        *,
        copy_builtin_instance: bool = False,
    ) -> type:
        """
        Build a builtin dataclass from a pydantic V1 BaseModel at runtime.
        If an instance is provided, an instance will be returned.
        If a definition is provided, a definition will be returned.
        :param bm: - the BaseModel to be rendered as an annotated (builtin) dataclass
        :param copy_builtin_instance: - special handling if the input is already an annotated (builtin) dataclass instance.
            if an annotated (builtin) dataclass definition is provided,
             then the provided definition is returned and this setting doesn't matter.
            if an annotated (builtin) dataclass instance is provided:
             and this setting is True, return a copy of the provided instance.
             and this setting is False (default), return the provided instance.
        """

        # prep and handle exception cases
        is_type = isinstance(bm, type)
        is_instance = not is_type
        tp = get_type(bm)

        # check to see if it is already an annotated (builtin or pydantic) dataclass
        if is_dataclass(tp):
            if is_instance:
                if copy_builtin_instance:
                    # return a shallow copy of the annotated dataclass instance
                    data = {field.name: getattr(bm, field.name) for field in dc_fields(bm)}
                    return tp(**data)
                # return the same annotated dataclass instance
                return bm
            else:
                # return the provided annotated dataclass definition
                return tp

        if not is_basemodel(tp):
            if is_type:
                message = f"Type {bm.__name__!r} is not a builtin dataclass."
            else:
                message = f"Instance of {type(bm).__name__!r} is not a builtin dataclass: {bm!r}"
            raise ValueError(message)

        # create the dataclass definition
        crossover_fields = {}

        # noinspection PyUnresolvedReferences
        for field_name, field_info in tp.__fields__.items():
            field_type = field_info.annotation
            field_default = field_info.default
            field_default_factory = field_info.default_factory
            field_required = field_info.required
            if field_required:
                # no default
                crossover_fields[field_name] = (field_name, field_type)
            else:
                if field_default is not None:
                    crossover_fields[field_name] = (field_name, field_type, field_default)
                elif field_default_factory is not None:
                    crossover_fields[field_name] = (
                        field_name,
                        field_type,
                        dc_field(default_factory=field_default_factory),
                    )
                else:
                    # optional - with a default value of `None`
                    crossover_fields[field_name] = (field_name, field_type, None)

        RuntimeDataclass = make_dataclass(
            builtin_dc_name(tp.__name__), [field_def for field_def in crossover_fields.values()]
        )

        # if it was a type, we're done
        if is_type:
            return RuntimeDataclass

        # otherwise, create the new instance
        bm_data: dict[str, Any] = bm.dict()
        # noinspection PyDataclass,PyTypeChecker
        data = {field.name: bm_data[field.name] for field in dc_fields(RuntimeDataclass)}
        runtime_dataclass = RuntimeDataclass(**data)

        return runtime_dataclass

else:

    # PYDANTIC_VERSION == "V2"
    from pydantic_core import PydanticUndefined  # noqa
    from pydantic._internal._model_construction import ModelMetaclass  # noqa

    def is_basemodel(model: object) -> bool:
        return isinstance(get_type(model), ModelMetaclass)

    def to_builtin_dc(
        bm: Any,
        *,
        copy_builtin_instance: bool = False,
    ) -> type:
        """
        Build a builtin dataclass from a pydantic V2 BaseModel at runtime.
        If an instance is provided, an instance will be returned.
        If a definition is provided, a definition will be returned.
        :param bm: - the BaseModel to be rendered as an annotated (builtin) dataclass
        :param copy_builtin_instance: - special handling if the input is already an annotated (builtin) dataclass instance.
            if an annotated (builtin) dataclass definition is provided,
             then the provided definition is returned and this setting doesn't matter.
            if an annotated (builtin) dataclass instance is provided:
             and this setting is True, return a copy of the provided instance.
             and this setting is False (default), return the provided instance.
        """

        # prep and handle exception cases
        is_type = isinstance(bm, type)
        is_instance = not is_type
        tp = get_type(bm)

        # check to see if it is already an annotated (builtin or pydantic) dataclass
        if is_dataclass(tp):
            if is_instance:
                if copy_builtin_instance:
                    # return a shallow copy of the annotated dataclass instance
                    data = {field.name: getattr(bm, field.name) for field in dc_fields(bm)}
                    return tp(**data)
                # return the same annotated dataclass instance
                return bm
            else:
                # return the provided annotated dataclass definition
                return tp

        # neither None nor NoneType is_basemodel
        if not is_basemodel(tp):
            if is_type:
                message = f"Type {bm.__name__!r} is not a pydantic BaseModel."
            else:
                message = f"Instance of {type(bm).__name__!r} is not a pydantic BaseModel: {bm!r}"
            raise ValueError(message)

        # create the dataclass definition
        crossover_fields = {}

        # noinspection PyUnresolvedReferences
        for field_name, field_info in tp.model_fields.items():
            field_type = field_info.annotation
            field_default = field_info.default
            field_default_factory = field_info.default_factory
            if field_default is not PydanticUndefined:
                # the field has a default value making it an optional field
                crossover_fields[field_name] = (field_name, field_type, field_default)
            elif field_default_factory is not None:
                # the field has a default_factory making it an optional field
                crossover_fields[field_name] = (
                    field_name,
                    field_type,
                    dc_field(default_factory=field_default_factory),
                )
            else:
                # No default, which makes it a required field
                crossover_fields[field_name] = (field_name, field_type)

        RuntimeDataclass = make_dataclass(
            builtin_dc_name(tp.__name__), [field_def for field_def in crossover_fields.values()]
        )

        # if it was a type, we're done
        if is_type:
            return RuntimeDataclass

        # otherwise, create the new instance
        bm_data: dict[str, Any] = bm.model_dump()
        # noinspection PyDataclass,PyTypeChecker
        data = {field.name: bm_data[field.name] for field in dc_fields(RuntimeDataclass)}
        runtime_dataclass = RuntimeDataclass(**data)

        return runtime_dataclass
