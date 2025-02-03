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
from byterover.api.resource.projects.types.project import Project
from byterover.api.core.pydantic_utilities import pydantic_v1


class NotesClient:
	def __init__(self, *, client_wrapper: SyncClientWrapper):
		self._client_wrapper = client_wrapper
	
	def check_note_exist(
		self,
		project_name,
		note_name,
		*,
		request_options: typing.Optional[RequestOptions] = None,
	) -> typing.List[Project]:
		"""
        Example: GET /api/brclient/notes/checkName?projectName=<project_name>&noteName=<note_name>
        """
		endpoint = "api/brclient/notes/checkName"
		params = {
			"projectName": project_name,
			"noteName": note_name
		}
		_response = self._client_wrapper.httpx_client.request(
			endpoint,
			params=params,
			method="GET",
			request_options=request_options,
		)
		try:
			if 200 <= _response.status_code < 300:
				data = _response.json()
				return [Project.parse_obj(item) for item in data]
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


class AsyncNotesClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def check_note_exist(
        self,
        project_name,
        note_name,
        *,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.Dict:
        """
        Example: GET /api/brclient/notes/checkName?projectName=<project_name>&noteName=<note_name>
        """
        endpoint = "api/brclient/notes/checkName"
        params = {
            "projectName": project_name,
            "noteName": note_name
        }
        _response = await self._client_wrapper.httpx_client.request(
            endpoint,
            params=params,
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                data = _response.json()  # remove 'await' here
                return data
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

    async def create_note(
        self,
        payload: dict,
        *,
        request_options: typing.Optional[RequestOptions] = None
    ) -> dict:
        """
        POST /api/byterover/note
        Expects `payload` in the shape the server requires.

        Returns the server's JSON response if status < 300.
        """
        endpoint = "api/byterover/note"
        _response = await self._client_wrapper.httpx_client.request(
            endpoint,
            method="POST",
            json=payload,
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return _response.json()
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

    async def check_usage_exceeded(
        self,
        *,
        request_options: typing.Optional[RequestOptions] = None
    ) -> typing.Dict:
        """
        GET /api/brclient/usage/exceeded
        Expects the API key (public/secret) to be included in the request headers.
        Returns a JSON object like: { "exceeded": false }.
        """
        endpoint = "api/brclient/usage/exceeded"
        _response = await self._client_wrapper.httpx_client.request(
            endpoint,
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                data = _response.json()  # remove 'await' here
                return data
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