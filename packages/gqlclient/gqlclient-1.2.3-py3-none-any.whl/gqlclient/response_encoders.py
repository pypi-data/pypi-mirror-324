"""
Encoders for translating a dict graphql response into another form
"""
import json
import logging

from dacite import Config
from dacite import from_dict

from gqlclient.exceptions import EncoderResponseException

__all__ = ["dataclass_encoder", "json_encoder", "dict_encoder"]

from gqlclient.pydantic_utils import is_basemodel

logger = logging.getLogger(__name__)


def dataclass_encoder(
    call_base: str,
    response: dict,
    response_cls: type,
) -> list[object] | object | None:
    """
    Response encoder that produces a list or a single instance of the response class

    :param call_base: The base query or mutation the response is coming from
    :param response: The dict response from the graphql server
    :param response_cls: The dataclass that was used to specify the response
    :return: An instance or list of instances of the response_cls instantiated with the graphql server response
    """

    def encode_response(raw_response: dict | list[dict]) -> object | list[object]:
        """
        encode the response of a dict or list
        """
        # Don't use dacite type checking, rely on pydantic dataclass for type checking if desired
        from_dict_config = Config(check_types=False)

        def render_response(raw_data: dict) -> object:
            """Return annotated (builtin or pydantic) dataclass or pydantic BaseModel depending on response_cls"""
            if is_basemodel(response_cls):
                return response_cls(**raw_data)
            # noinspection PyTypeChecker
            return from_dict(response_cls, raw_data, from_dict_config)

        if isinstance(raw_response, list):
            return [render_response(row) for row in raw_response]
        else:
            return render_response(raw_response)

    if response_cls is None:  # no response was desired
        return None
    response = response[call_base]  # index into the payload of the response for the call
    try:
        encoded_response = encode_response(response)
    except Exception as e:
        logger.error(f"Error dataclass encoding response: detail={e}")
        raise EncoderResponseException(str(e))
    return encoded_response


def json_encoder(
    call_base: str,
    response: list[dict] | dict,
    response_cls: type,
) -> str:
    """
    Response encoder that produces json string

    :param call_base: The base query or mutation the response is coming from
    :param response: The dict response from the graphql server
    :param response_cls: The dataclass that was used to specify the response
    :return: A json formatted string of the dict response
    """
    try:
        result = json.dumps(response)
    except TypeError as e:
        logger.error(f"Error json encoding response: detail={e}")
        raise EncoderResponseException(str(e))
    return result


def dict_encoder(
    call_base: str,
    response: list[dict] | dict,
    response_cls: type,
) -> list[dict] | dict:
    """
    Default encoder which returns the response as a dict or list of dicts

    :param call_base: The base query or mutation the response is coming from
    :param response: The dict response from the graphql server
    :param response_cls: The dataclass that was used to specify the response
    :return: A json formatted string of the dict response
    :raises EncoderResponseException: Raised when the response is not a dict
    or list
    """
    if isinstance(response, (dict, list)):
        return response
    raise EncoderResponseException("Response parameter is expected to be a dict or list")
