from typing import Optional

import typer
from rich.console import Console

from byterover._utils.async_utils import synchronizer
from byterover.cli.utils import display_table
from byterover.config import config_set_active_profile, _profile, config_profiles

profile_cli = typer.Typer(name="profile", help="Switch between Byterover profiles.", no_args_is_help=True)

@profile_cli.command(name="activate", help="Activate one Byterover profile.")
def activate(profile: str = typer.Argument(..., help="Byterover profile to activate.")):
    config_set_active_profile(profile)

@profile_cli.command(name="current", help="Show the currently active Byterover profile.")
def current():
    console = Console()
    console.print("[bold]Current Activated Profile:[/bold]")
    console.print(f"Profile Name: [green]{_profile}[/green]")


@profile_cli.command(name="list", help="Show all Byterover profiles and highlight the active one.")
@synchronizer.create_blocking
async def list_():
    profiles = config_profiles()
    colum_names = ["Profile Name", "Active"]
    rows = []
    for profile in profiles:
        active = "•" if profile == _profile else ""
        rows.append([profile, active])
    display_table(colum_names, rows, title="Profiles")
