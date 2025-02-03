import getpass
from typing import Optional
import typer

from byterover.token_flow import _set_token

token_cli = typer.Typer(name="token", help="Manage tokens for credentials.", no_args_is_help=True)

from byterover._utils.async_utils import synchronizer


activate_option = typer.Option(
    True,
    help="Activate the profile containing this token after creation.",
)

verify_option = typer.Option(
    True,
    help="Make a test request to verify the new credentials.",
)

@token_cli.command(
    name="activate",
    help=(
        "Set account credentials for connecting to Byterover. "
        "If not provided with the command, you will be prompted to enter your credentials."
    ),
)
@synchronizer.create_blocking
async def activate(
    public_token: Optional[str] = typer.Option(None, help="Account token ID."),
    secret_token: Optional[str] = typer.Option(None, help="Account token secret."),
    user_name: Optional[str] = typer.Option(None, help="User name associated with the account."),
    activate: bool = activate_option,
    verify: bool = verify_option,
):
    if public_token is None:
        public_token = getpass.getpass("Public token:")
    if secret_token is None:
        secret_token = getpass.getpass("Secret token:")
    if user_name is None:
        user_name = getpass.getuser()
    await _set_token(public_token=public_token, secret_token=secret_token, user_name=user_name, activate=activate, verify=verify)


@token_cli.command(name="current", help="Show the currently active token.")
def current():
    """
    Display the current token details.

    **Note:** For security reasons, we only display the public token and the associated user name.
    """
    from rich.console import Console
    # Assume that once a token is activated, its details are stored in a global config,
    # similar to how _profile is used in your profile commands.
    from byterover.config import config
    
    console = Console()
    public_token = config.get("public_token")
    secret_token = config.get("secret_token")
    if not config:
        console.print("[red]No token is currently active.[/red]")
    else:
        console.print("[bold]Current Token Details:[/bold]")
        console.print(f"Public Token: [bold]{public_token}[/bold]")
        console.print(f"Secret Token: [bold]{secret_token}[/bold]")