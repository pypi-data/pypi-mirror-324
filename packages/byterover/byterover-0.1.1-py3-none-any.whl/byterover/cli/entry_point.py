import typer

from byterover.cli.profile import profile_cli
from byterover.cli.run import run_cli
from byterover.cli.token import token_cli
from byterover.cli.project import project_cli
from byterover.cli.llm_key import llm_key_cli

def version_callback(value: bool):
	if value:
		from byterover_version import __version__
		typer.echo(f"Byterover client version: {__version__}")
		raise typer.Exit()

entrypoint_cli_typer = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    rich_markup_mode="markdown",
    help="""
    Byterover is the most convenient way to track your code evolution.

    See the website at https://byterover.dev/ for documentation and more information
    about tracking code evolution on Byterover.
    """,
)

@entrypoint_cli_typer.callback()
def byterover(
    ctx: typer.Context,
    version: bool = typer.Option(None, "--version", callback=version_callback),
):
	pass

#run
entrypoint_cli_typer.add_typer(run_cli, rich_help_panel="Run the Byterover CLI process.")

# Configuration
entrypoint_cli_typer.add_typer(token_cli, rich_help_panel="Configuration")
entrypoint_cli_typer.add_typer(project_cli, rich_help_panel="Configuration")
entrypoint_cli_typer.add_typer(profile_cli, rich_help_panel="Configuration")
entrypoint_cli_typer.add_typer(llm_key_cli, rich_help_panel="Configuration")

entrypoint_cli = typer.main.get_command(entrypoint_cli_typer)
entrypoint_cli.list_commands(None)

if __name__ == "__main__":
	# this module is only called from tests, otherwise the parent package __main__.py is used as the entrypoint
    entrypoint_cli()