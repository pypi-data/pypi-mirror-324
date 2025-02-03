from typing import Optional

import typer

from byterover._utils.async_utils import synchronizer
from byterover.api.client import AsyncByteroverClient
from byterover.api.resource.tokens import VerifyTokenRequest
from byterover.cli.utils import display_table
from byterover.config import config, _store_user_config

llm_key_cli = typer.Typer(name="llm_key", help="Manage llm keys.", no_args_is_help=True)


@llm_key_cli.command("list", help="Display all available LLM API keys.")
@synchronizer.create_blocking
async def list_(json: Optional[bool] = False):
	async_byterover_client = AsyncByteroverClient.from_env()
	llm_keys = await async_byterover_client.llm_keys.get_all_for_organization()
	
	column_names = ["Id", "LLM KeyName", "Created at"]
	rows = []
	
	for item in llm_keys:
		rows.append(
			[
				item.id,
				item.provider,
				str(item.createdAt)
			]
		)
	display_table(column_names, rows, json, title="LLM Keys")


@llm_key_cli.command("activate", help="Set the current LLM API key.")
@synchronizer.create_blocking
async def activate_llm_key(
	llm_key_name: str = typer.Argument(..., help="LLM API Key name to set as current."),
):
	"""
	Update the local Byterover config with a chosen LLM API key.

	This command verifies that the provided key exists in your organization
	and, if so, stores it in the configuration as the active LLM key.
	"""
	async_byterover_client = AsyncByteroverClient.from_env()
	c = config
	public_token = c.get("public_token")
	secret_token = c.get("secret_token")
	
	# Verify tokens to ensure access to organization details.
	verify = await async_byterover_client.tokens.verify(
		request=VerifyTokenRequest(publicKey=public_token, secretKey=secret_token)
	)
	org_id = verify.organizationId
	
	# Retrieve the available LLM keys.
	llm_keys = await async_byterover_client.llm_keys.get_all_for_organization()
	if llm_key_name not in [k.provider for k in llm_keys]:
		typer.echo(f"LLM Key '{llm_key_name}' not found in org '{org_id}'. Aborting.")
		raise typer.Exit(1)
	
	# Store the selected LLM key in the configuration.
	_store_user_config({"llm_key_name": llm_key_name}, active_profile=None)
	
	typer.echo(f"LLM Key '{llm_key_name}' set as current.")


@llm_key_cli.command("current", help="Show the currently active LLM API key.")
def current():
	"""
	Display the currently active LLM API key from the configuration.

	For security and clarity, only the key's name is shown.
	"""
	from rich.console import Console
	llm_key_name = config.get("llm_key_name")
	console = Console()
	if not llm_key_name:
		console.print("[red]No LLM API key is currently active.[/red]")
	else:
		console.print("[bold]Current Active LLM API Key:[/bold]")
		console.print(f"LLM API Key Name: [green]{llm_key_name}[/green]")