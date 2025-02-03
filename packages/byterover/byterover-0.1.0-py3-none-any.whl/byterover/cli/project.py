from typing import Optional

import typer

from byterover._utils.async_utils import synchronizer
from byterover.api.client import AsyncByteroverClient
from byterover.api.resource.tokens import VerifyTokenRequest
from byterover.cli.utils import display_table
from byterover.config import config, _store_user_config

project_cli = typer.Typer(name="project", help="Manage projects.", no_args_is_help=True)

@project_cli.command("list", help="List your projects in the current organization.")
@synchronizer.create_blocking
async def list_(json: Optional[bool] = False):
    async_byterover_client = AsyncByteroverClient.from_env()
    response = await async_byterover_client.projects.get_all_for_organization()
    colum_names = ["Id", "Project name", "Created at", "Updated at"]
    rows = []
    
    for item in response:
        rows.append(
            [
                item.id,
                item.name,
                str(item.createdAt),
                str(item.updatedAt)
            ]
        )
    display_table(colum_names, rows, json, title="Projects")

@project_cli.command("activate", help="Activate the current project for the Byterover CLI.")
@synchronizer.create_blocking
async def activate_project(
    project_name: str = typer.Argument(..., help="Project Name to activate."),
):
    """
    Update the local Byterover config with a chosen project_id.
    """
    async_byterover_client = AsyncByteroverClient.from_env()
    c = config
    public_token = c.get("public_token")
    secret_token = c.get("secret_token")
    resp = await async_byterover_client.tokens.verify(
        request=VerifyTokenRequest(publicKey=public_token, secretKey=secret_token)
    )
    org_id = resp.organizationId
    # check if project_id is in the user's list
    projects = await async_byterover_client.projects.get_all_for_organization()
    if project_name not in [p.name for p in projects]:
        typer.echo(f"Project '{project_name}' not found in org '{org_id}'. Aborting.")
        raise typer.Exit(1)
    
    # Store project_id in the config
    _store_user_config({"project_name": project_name}, active_profile=None)
    
    typer.echo(f"Activate the project: {project_name}")


@project_cli.command("current", help="Show the currently active project.")
def current():
    """
    Display the currently activated project.

    This command retrieves the 'project_name' from the configuration and displays it.
    """
    from rich.console import Console
    # Get the current project name from the config
    project_name = config.get("project_name")
    
    console = Console()
    if not project_name:
        console.print("[red]No project is currently active.[/red]")
    else:
        console.print("[bold]Current Activated Project:[/bold]")
        console.print(f"Project Name: [green]{project_name}[/green]")