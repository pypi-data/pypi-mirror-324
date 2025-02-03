import httpx

import typing

from byterover.api.resource.llm_keys.client import AsyncLlmKeysClient, LlmKeysClient
from byterover.api.resource.notes.client import AsyncNotesClient
from byterover.api.resource.organizations.client import OrganizationsClient, AsyncOrganizationsClient
from byterover.api.resource.projects.client import ProjectsClient, AsyncProjectsClient
from byterover.api.resource.tokens.client import TokensClient, AsyncTokensClient
from byterover.api.core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from byterover.config import _check_config, config
from byterover.config import BYTEROVER_SERVER_URL, STARGATE_SERVER_URL

class ByteroverClient:
	def __init__(
		self,
		*,
		base_url: str,
		public_token: typing.Optional[str] = None,
		secret_token: typing.Optional[str] = None,
		username: typing.Optional[typing.Union[str, typing.Callable[[], str]]] = None,
		timeout: typing.Optional[float] = None,
		follow_redirects: typing.Optional[bool] = True,
		httpx_client: typing.Optional[httpx.Client] = None
	):
		
		_defaulted_timeout=(
			timeout if timeout is not None else 60 if httpx_client is None else None
		)
		self._client_wrapper = SyncClientWrapper(
			base_url=base_url,
			public_token=public_token,
			secret_token=secret_token,
			username=username,
			httpx_client=httpx_client
			if httpx_client is not None
			else httpx.Client(
				timeout=_defaulted_timeout,
				follow_redirects=follow_redirects,
			),
			timeout=_defaulted_timeout,
		)
		self.tokens = TokensClient(client_wrapper=self._client_wrapper)
		self.organizations = OrganizationsClient(client_wrapper=self._client_wrapper)
		self.projects = ProjectsClient(client_wrapper=self._client_wrapper)
		self.llm_keys = LlmKeysClient(client_wrapper=self._client_wrapper)
	@classmethod
	async def from_env(cls) -> "ByteroverClient":
		base_url = BYTEROVER_SERVER_URL
		_check_config()
		c = config
		public_token = c.get("public_token")
		secret_token = c.get("secret_token")
		username = c.get("user_name")
		return cls(
			base_url=base_url,
			public_token=public_token,
			secret_token=secret_token,
			username=username,
		)



class AsyncByteroverClient:
	def __init__(
		self,
		*,
		base_url: str,
		public_token: typing.Optional[str] = None,
		secret_token: typing.Optional[str] = None,
		username: typing.Optional[typing.Union[str, typing.Callable[[], str]]] = None,
		timeout: typing.Optional[float] = None,
		follow_redirects: typing.Optional[bool] = True,
		httpx_client: typing.Optional[httpx.AsyncClient] = None
	):
		_defaulted_timeout=(
			timeout if timeout is not None else 60 if httpx_client is None else None
		)
		
		self._client_wrapper = AsyncClientWrapper(
			base_url=base_url,
			public_token=public_token,
			secret_token=secret_token,
			username=username,
			httpx_client=httpx_client
			if httpx_client is not None
			else httpx.AsyncClient(
				timeout=_defaulted_timeout,
				follow_redirects=follow_redirects,
			),
			timeout=_defaulted_timeout,
		)
		self.tokens = AsyncTokensClient(client_wrapper=self._client_wrapper)
		self.organizations = AsyncOrganizationsClient(client_wrapper=self._client_wrapper)
		self.projects = AsyncProjectsClient(client_wrapper=self._client_wrapper)
		self.llm_keys = AsyncLlmKeysClient(client_wrapper=self._client_wrapper)
		self.notes = AsyncNotesClient(client_wrapper=self._client_wrapper)
	
	@classmethod
	def from_env(cls) -> "AsyncByteroverClient":
		base_url = BYTEROVER_SERVER_URL
		_check_config()
		c = config
		public_token = c.get("public_token")
		secret_token = c.get("secret_token")
		username = c.get("user_name")
		return cls(
			base_url=base_url,
			public_token=public_token,
			secret_token=secret_token,
			username=username,
		)

class AsyncStargateClient:
	def __init__(
		self,
		httpx_client: typing.Optional[httpx.AsyncClient] = None,
		timeout: typing.Optional[float] = None,
		follow_redirects: bool = True,
	):
		# If no client is passed, create a default one with a fallback timeout.
		if httpx_client is None:
			_default_timeout = 60 if timeout is None else timeout
			httpx_client = httpx.AsyncClient(
				timeout=_default_timeout,
				follow_redirects=follow_redirects,
			)

		self._client_wrapper = AsyncClientWrapper(
			base_url=STARGATE_SERVER_URL,
			public_token=config.get("public_token"),
			secret_token=config.get("secret_token"),
			username=config.get("user_name"),
			httpx_client=httpx_client,
			timeout=timeout,
		)
		self.notes = AsyncNotesClient(client_wrapper=self._client_wrapper)

	@classmethod
	def from_env(cls) -> "AsyncStargateClient":
		"""
		Create a StargateClient from environment/config settings.
		No external httpx_client passed => we'll auto-create one.
		"""
		return cls()