import os
from typing import Optional
from rich.console import Console

from byterover.api.resource.tokens import VerifyTokenRequest
from byterover.config import config_profiles, user_config_path, _store_user_config, config
from byterover.exception import AuthError
from byterover.api.client import AsyncByteroverClient

async def _set_token(
    *,
    public_token: str,
    secret_token: str,
    user_name: str,
    profile: Optional[str] = None,
    activate: bool = True,
    verify: bool = True,
):
    byterover_server_url = config.get("byterover_server_url", profile=profile)
    async_byterover_client = AsyncByteroverClient(base_url=byterover_server_url, public_token=public_token, secret_token=secret_token)
    console = Console()  # Initialize Console outside the if block
    if verify:
        console.print(f"Verifying token against [blue]{byterover_server_url}[/blue]")
        await async_byterover_client.tokens.verify(request=VerifyTokenRequest(publicKey=public_token, secretKey=secret_token))
        
        console.print("[green]Token verified successfully![/green]")

    if profile is None:
        if "BYTEROVER_PROFILE" in os.environ:
            profile = os.environ["BYTEROVER_PROFILE"]
        else:
            try:
                organization = await async_byterover_client.organizations.get()
            except AuthError as exc:
                if not verify:
                    # Improve the error message for verification failure with --no-verify to reduce surprise
                    msg = "No profile name given, but could not authenticate client to look up organization name."
                    raise AuthError(msg) from exc
                raise exc
            profile = organization.name

    config_data = {"public_token": public_token, "secret_token": secret_token, "user_name": user_name}
    
    # Activate the profile when requested or if no other profiles currently exist
    active_profile = profile if (activate or not config_profiles()) else None
    with console.status("Storing token", spinner="dots"):
        _store_user_config(config_data, profile=profile, active_profile=active_profile)
    console.print(
        f"[green]Token written to [magenta]{user_config_path}[/magenta] in profile "
        f"[magenta]{profile}[/magenta].[/green]"
    )
