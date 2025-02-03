import typing
from json import JSONDecodeError

from byterover.api.core.api_error import ApiError
from byterover.api.core.client_wrapper import SyncClientWrapper, AsyncClientWrapper
from byterover.api.core.request_options import RequestOptions
from byterover.api.resource.commons.errors import UnauthorizedError, AccessDeniedError, MethodNotAllowedError
from byterover.api.resource.organizations import Organization
from byterover.exception import Error, NotFoundError

class OrganizationsClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def get(
        self,
        *,
        request_options: typing.Optional[RequestOptions] = None
    ) -> Organization:
        """
        Get Organization associated with API key
        """
        _response = self._client_wrapper.httpx_client.request(
            "api/brclient/organizations/organization",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return Organization.parse_obj(_response.json())
            if _response.status_code == 400:
                raise Error(_response.json())
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
    
    def get_all(
        self,
        *,
        request_options: typing.Optional[RequestOptions] = None
    ) -> typing.List[Organization]:
        """
        Get all Organizations
        """
        _response = self._client_wrapper.httpx_client.request(
            "api/brclient/organizations",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                data = _response.json()
                return [Organization.parse_obj(item) for item in data]
            if _response.status_code == 400:
                raise Error(_response.json())
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

class AsyncOrganizationsClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def get(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> Organization:
        """
        Get Organization associated with API key in async
        """
        _response = await  self._client_wrapper.httpx_client.request(
            "api/brclient/organizations/organization",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return Organization.parse_obj(_response.json())
            if _response.status_code == 400:
                raise Error(_response.json())
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
    
    async def get_all(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.List[Organization]:
        """
        Get all Organizations in async
        """
        _response = await self._client_wrapper.httpx_client.request(
            "api/brclient/organizations",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                data = _response.json()
                return [Organization.parse_obj(item) for item in data]
            if _response.status_code == 400:
                raise Error(_response.json())
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