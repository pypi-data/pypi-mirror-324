import subprocess
import json
import typer

from yaspin import yaspin

from byterover._utils.async_utils import synchronizer
from byterover.api.client import AsyncByteroverClient, AsyncStargateClient
from byterover.config import config

run_cli = typer.Typer(name="run", help="Run the Byterover CLI process.")


@run_cli.command("note")
@synchronizer.create_blocking
async def note(
	commit: str = typer.Option(
		None,
		"--commit",
		"-c",
		help="Optional commit hash to process. Defaults to the latest commit if not provided."
	)
):
	"""
    Gathers local Git info (branch, commit, diff, etc.),
    checks the note existence via the AsyncByteroverClient,
    and before creating the note, verifies that the free-plan usage has not been exceeded.

    The payload includes the commit hash, and if the --commit option is specified,
    that commit will be processed; otherwise, the latest commit is used.
    """
	# 1) Load config and validate credentials
	c = config
	public_token = c.get("public_token")
	secret_token = c.get("secret_token")
	if not public_token or not secret_token:
		typer.echo("Error: No public/secret key in config. Please log in or set tokens.")
		raise typer.Exit(1)
	
	# 2) Extract Git info
	try:
		branch_name = subprocess.check_output(
			["git", "rev-parse", "--abbrev-ref", "HEAD"],
			encoding="utf-8"
		).strip()
		
		# Use the provided commit hash or default to the latest commit.
		commit_hash = commit if commit else subprocess.check_output(
			["git", "rev-parse", "HEAD"],
			encoding="utf-8"
		).strip()
		
		commit_message = subprocess.check_output(
			["git", "log", "-1", "--pretty=%B", commit_hash],
			encoding="utf-8"
		).strip()
		
		# Calculate the diff: compare the commit against its immediate parent.
		# (If the commit is the first commit, this might fail; you could handle that separately.)
		try:
			code_diff = subprocess.check_output(
				["git", "diff", f"{commit_hash}~1", commit_hash],
				encoding="utf-8"
			)
		except subprocess.CalledProcessError:
			code_diff = ""  # If diff fails (e.g. for the initial commit), use an empty string.
		
		user_name = subprocess.check_output(
			["git", "config", "user.name"],
			encoding="utf-8"
		).strip()
	
	except Exception as exc:
		typer.echo(f"Error reading data from Git: {exc}")
		raise typer.Exit(1)
	
	# 3) Ensure we have a project name
	project_name = c.get("project_name")
	if not project_name:
		typer.echo("Error: No project_name found in config. Please run 'byterover project set <name>'.")
		raise typer.Exit(1)
	
	# 4) LLM key name
	llm_provider = c.get("llm_key_name") or "anthropic"
	
	# 5) Create the Byterover client
	async_byterover_client = AsyncByteroverClient.from_env()
	
	# 5.5) Check usage via the notes client method.
	try:
		usage_data = await async_byterover_client.notes.check_usage_exceeded()
	except Exception as e:
		typer.echo(f"Error checking usage: {e}")
		raise typer.Exit(1)
	
	if usage_data.get("exceeded"):
		typer.echo("Usage limit exceeded. Please upgrade your plan before creating a note.")
		raise typer.Exit(1)
	
	# 6) Check if a note already exists using a unique note identifier.
	# Here, we use a combination of the branch name and commit hash.
	note_identifier = f"{branch_name}"
	try:
		check_result = await async_byterover_client.notes.check_note_exist(
			project_name=project_name,
			note_name=note_identifier,
		)
		note_exists = check_result.get("exists", False)
	except Exception as e:
		typer.echo(f"Error checking note name: {e}")
		raise typer.Exit(1)
	
	need_to_create_new_note = not note_exists
	
	# 7) Construct final payload for the note.
	payload = {
		"branch_name": branch_name,
		"commit_hash": commit_hash,
		"user_name": user_name,
		"project_name": project_name,
		"commit_message": commit_message,
		"code_diff": code_diff,
		"need_to_create_new_note": need_to_create_new_note,
		"llm_provider": llm_provider,
	}
	
	# 8) Create the note via the Stargate client.
	stargate_client = AsyncStargateClient.from_env()
	
	with yaspin(text="Creating your note on Byterover...", color="cyan") as spinner:
		try:
			response = await stargate_client.notes.create_note(payload=payload)
			spinner.ok("✅  Your note should be ready shortly!")
			typer.echo("Server responded:")
			typer.echo(json.dumps(response, indent=2))
		except Exception as e:
			spinner.fail(f"💥  Error creating note via Stargate: {e}")
			raise typer.Exit(1)