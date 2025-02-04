import typing
from json import JSONDecodeError

from byterover.api.core.api_error import ApiError
from byterover.api.core.client_wrapper import SyncClientWrapper, AsyncClientWrapper
from byterover.api.core.request_options import RequestOptions
from byterover.api.resource.commons.errors import (
    UnauthorizedError,
    AccessDeniedError,
    MethodNotAllowedError,
    NotFoundError,
    Error,
)
from byterover.api.core.pydantic_utilities import pydantic_v1
from byterover.api.resource.llm_keys.types.llm_key import LlmKey

class LlmKeysClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def get_all_for_organization(
        self,
        *,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.List[LlmKey]:
        """
        Get all LLM keys for a given organization (sync).
        """
        endpoint = f"api/brclient/organizations/llmKeys"
        _response = self._client_wrapper.httpx_client.request(
            endpoint,
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                data = _response.json()
                return [LlmKey.parse_obj(item) for item in data]
            if _response.status_code == 400:
                raise Error(pydantic_v1.BaseModel.parse_obj(_response.json()))
            if _response.status_code == 401:
                raise UnauthorizedError(_response.json())
            if _response.status_code == 403:
                raise AccessDeniedError(_response.json())
            if _response.status_code == 405:
                raise MethodNotAllowedError(_response.json())
            if _response.status_code == 404:
                raise NotFoundError(_response.json())
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncLlmKeysClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def get_all_for_organization(
        self,
        *,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.List[LlmKey]:
        """
        Get all LLM keys for a given organization (async).
        """
        endpoint = f"api/brclient/organizations/llmKeys"
        _response = await self._client_wrapper.httpx_client.request(
            endpoint,
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                data = _response.json()
                return [LlmKey.parse_obj(item) for item in data]
            if _response.status_code == 400:
                raise Error(pydantic_v1.BaseModel.parse_obj(_response.json()))
            if _response.status_code == 401:
                raise UnauthorizedError(_response.json())
            if _response.status_code == 403:
                raise AccessDeniedError(_response.json())
            if _response.status_code == 405:
                raise MethodNotAllowedError(_response.json())
            if _response.status_code == 404:
                raise NotFoundError(_response.json())
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)