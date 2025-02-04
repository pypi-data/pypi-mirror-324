import typing
from json import JSONDecodeError

from byterover.api.core.api_error import ApiError
from byterover.api.core.client_wrapper import SyncClientWrapper, AsyncClientWrapper
from byterover.api.core.request_options import RequestOptions
from byterover.api.resource.commons.errors import UnauthorizedError, AccessDeniedError, MethodNotAllowedError, \
	NotFoundError, Error
from byterover.api.resource.tokens import VerifyTokenRequest, VerifyTokenResponse
from byterover.api.core.pydantic_utilities import pydantic_v1

class TokensClient:
	def __init__(self, *, client_wrapper: SyncClientWrapper):
		self._client_wrapper = client_wrapper
	
	def verify(
		self,
		*,
		request: VerifyTokenRequest,
		request_options: typing.Optional[RequestOptions] = None,
	) -> VerifyTokenResponse:
		
		_response = self._client_wrapper.httpx_client.request(
			"api/brclient/apiKeys/verify",
			method="POST",
			json=request,
			request_options=request_options,
		)
		try:
			if 200 <= _response.status_code < 300:
				return VerifyTokenResponse.parse_obj(_response.json())
			if _response.status_code == 400:
				raise Error(pydantic_v1.BaseModel.parse_obj(_response.json()))
			if _response.status_code == 401:
				raise UnauthorizedError(
					pydantic_v1.BaseModel.parse_obj(_response.json())
				)
			if _response.status_code == 403:
				raise AccessDeniedError(
					pydantic_v1.BaseModel.parse_obj(_response.json())
				)
			if _response.status_code == 405:
				raise MethodNotAllowedError(
					pydantic_v1.BaseModel.parse_obj(_response.json())
				)
			if _response.status_code == 404:
				raise NotFoundError(
					pydantic_v1.BaseModel.parse_obj(_response.json())
				)
			_response_json = _response.json()
		except JSONDecodeError:
			raise ApiError(status_code=_response.status_code, body=_response.text)
		raise ApiError(status_code=_response.status_code, body=_response_json)
	
class AsyncTokensClient:
	def __init__(self, *, client_wrapper: AsyncClientWrapper):
		self._client_wrapper = client_wrapper
	
	async def verify(
		self,
		*,
		request: VerifyTokenRequest,
		request_options: typing.Optional[RequestOptions] = None,
	) -> VerifyTokenResponse:
		_response = await self._client_wrapper.httpx_client.request(
			"api/brclient/apiKeys/verify",
			method="POST",
			json={
				"publicKey": request.publicKey,
				"secretKey": request.secretKey,
			},
			request_options=request_options,
		)
		try:
			if 200 <= _response.status_code < 300:
				return VerifyTokenResponse.parse_obj(_response.json())
			if _response.status_code == 400:
				raise Error(pydantic_v1.BaseModel.parse_obj(_response.json()))
			if _response.status_code == 401:
				raise UnauthorizedError(
					pydantic_v1.BaseModel.parse_obj(_response.json())
				)
			if _response.status_code == 403:
				raise AccessDeniedError(
					pydantic_v1.BaseModel.parse_obj(_response.json())
				)
			if _response.status_code == 405:
				raise MethodNotAllowedError(
					pydantic_v1.BaseModel.parse_obj(_response.json())
				)
			if _response.status_code == 404:
				raise NotFoundError(
					pydantic_v1.BaseModel.parse_obj(_response.json())
				)
			_response_json = _response.json()
		except JSONDecodeError:
			raise ApiError(status_code=_response.status_code, body=_response.text)
		raise ApiError(status_code=_response.status_code, body=_response_json)