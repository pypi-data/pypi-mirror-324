from importlib.metadata import version
from importlib.util import find_spec
from typing import Literal

from packaging import version as packaging_version


def pydantic_loaded() -> bool:
    """True if pydantic is loaded"""
    loaded = find_spec("pydantic")
    return bool(loaded)


PYDANTIC_LOADED = pydantic_loaded()
PYDANTIC_NOT_LOADED = not PYDANTIC_LOADED


def pydantic_version() -> Literal["NOT_LOADED", "V1", "V2"]:
    if PYDANTIC_NOT_LOADED:
        return "NOT_LOADED"
    loaded_pydantic_version = packaging_version.parse(version("pydantic"))
    if loaded_pydantic_version.major == 1:
        return "V1"
    if loaded_pydantic_version.major == 2:
        return "V2"
    raise RuntimeError(f"Unsupported pydantic version: {loaded_pydantic_version!r}")


PYDANTIC_VERSION = pydantic_version()
