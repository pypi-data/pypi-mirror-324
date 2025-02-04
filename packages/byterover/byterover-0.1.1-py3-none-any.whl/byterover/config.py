# Locate config file and read it
import os
import typing
import logging
import warnings
from textwrap import dedent

import toml

from byterover._utils.deprecation import deprecation_error
from byterover.exception import InvalidError
from byterover._utils.logger import configure_logger
from typing import Any, Optional

# 1) Figure out the absolute path to config.toml
CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "..",  # up one directory from byterover/
    "config.toml"
)
# 2) Attempt to load it
try:
    with open(CONFIG_PATH, "r") as f:
        _raw_config = toml.load(f)
except FileNotFoundError:
    raise RuntimeError(f"Could not find config.toml at '{CONFIG_PATH}'")
except Exception as e:
    raise RuntimeError(f"Error loading config.toml: {e}")

# 3) Extract the relevant sections.
#    We assume `[url]` table holds byterover_server_url and stargate_server_url.
_url_section = _raw_config.get("url", {})

# 4) Provide public constants or variables for the rest of your code
BYTEROVER_SERVER_URL = _url_section.get("byterover_server_url", "dev.byterover.dev")
STARGATE_SERVER_URL = _url_section.get("stargate_server_url", "ai.byterover.dev")

user_config_path: str = os.environ.get("BYTEROVER_CONFIG_PATH") or os.path.expanduser("~/.byterover.toml")

def _read_user_config():
    config_data = {}
    if os.path.exists(user_config_path):
        # Defer toml import so we don't need it in the container runtime environment
        import toml

        try:
            with open(user_config_path) as f:
                config_data = toml.load(f)
        except Exception as exc:
            config_problem = str(exc)
        else:
            if not all(isinstance(e, dict) for e in config_data.values()):
                config_problem = "TOML file must contain table sections for each profile."
            else:
                config_problem = ""
        if config_problem:
            message = f"\nError when reading the byterover configuration from `{user_config_path}`.\n\n{config_problem}"
            raise InvalidError(message)
    return config_data

_user_config = _read_user_config()


def config_profiles():
    """List the available byterover profiles in the .byterover.toml file."""
    return _user_config.keys()

def _config_active_profile() -> str:
    for key, values in _user_config.items():
        if values.get("active", False) is True:
            return key
    else:
        return "default"

def config_set_active_profile(profile: str) -> None:
    """Set the user's active Byterover profile by writing it to the `.byterover.toml` file."""
    from rich.console import Console
    console = Console()

    if profile not in _user_config:
        available_profiles = ", ".join(_user_config.keys())
        console.print(
            f"[red]Profile '{profile}' not found. Available profiles are: {available_profiles}[/red]"
        )
        return

    # Remove the active flag from all profiles.
    for key, values in _user_config.items():
        values.pop("active", None)

    # Set the requested profile as active.
    _user_config[profile]["active"] = True
    _write_user_config(_user_config)
    console.print(f"[green]Profile '{profile}' has been successfully activated.[/green]")

def _check_config() -> None:
    num_profiles = len(_user_config)
    num_active = sum(v.get("active", False) for v in _user_config.values())
    if num_active > 1:
        raise InvalidError(
            "More than one Byterover profile is active. "
            "Please fix with `Byterover profile activate` or by editing your Byterover config file "
            f"({user_config_path})."
        )
    elif num_profiles > 1 and num_active == 0 and _profile == "default":
        # Eventually we plan to have num_profiles > 1 with num_active = 0 be an error
        # But we want to give users time to activate one of their profiles without disruption
        message = dedent(
            """
            Support for using an implicit 'default' profile is deprecated.
            Please use fixed profile names and activate one of them by editing your Byterover config file
             """ + f"({user_config_path})."
        )
        deprecation_error((2024, 2, 6), message)


_profile = os.environ.get("BYTEROVER_PROFILE") or _config_active_profile()


class _Setting(typing.NamedTuple):
    default: typing.Any = None
    transform: typing.Callable[[str], typing.Any] = lambda x: x

_SETTINGS = {
    "loglevel": _Setting("WARNING", lambda s: s.upper()),
    "log_format": _Setting("STRING", lambda s: s.upper()),
    "byterover_server_url": _Setting(BYTEROVER_SERVER_URL),
    "stargate_server_url": _Setting(STARGATE_SERVER_URL),
    "public_token": _Setting(),
    "secret_token": _Setting(),
    "user_name": _Setting(),
    "project_name": _Setting(),
    "llm_key_name": _Setting(),
}

class Config:
    """Singleton that holds configuration used by BYTEROVER internally."""

    def __init__(self):
        pass

    def get(self, key, profile=None):
        """Looks up a configuration value.
        """
        if profile is None:
            profile = _profile
        s = _SETTINGS[key]
        if profile in _user_config and key in _user_config[profile]:
            return s.transform(_user_config[profile][key])
        else:
            return s.default

    def override_locally(self, key: str, value: str):
        # Override setting in this process by overriding variable for the setting
        #
        # Does NOT write back to settings file etc.
        try:
            self.get(key)
            os.environ["BYTEROVER_" + key.upper()] = value
        except KeyError:
            # Override env vars not available in config, e.g. NVIDIA_VISIBLE_DEVICES.
            # This is used for restoring env vars from a memory snapshot.
            os.environ[key.upper()] = value

    def __getitem__(self, key):
        return self.get(key)

    def __repr__(self):
        return repr(self.to_dict())

    def to_dict(self):
        return {key: self.get(key) for key in sorted(_SETTINGS)}


config = Config()

# Logging

logger = logging.getLogger("byterover-client")
configure_logger(logger, config["loglevel"], config["log_format"])

# Utils to write config


def _store_user_config(
    new_settings: dict[str, Any], profile: Optional[str] = None, active_profile: Optional[str] = None
):
    """Internal method, used by the CLI to set tokens."""
    if profile is None:
        profile = _profile
    user_config = _read_user_config()
    user_config.setdefault(profile, {}).update(**new_settings)
    if active_profile is not None:
        for prof_name, prof_config in user_config.items():
            if prof_name == active_profile:
                prof_config["active"] = True
            else:
                prof_config.pop("active", None)
    _write_user_config(user_config)


def _write_user_config(user_config):
    # Defer toml import so we don't need it in the container runtime environment
    import toml

    with open(user_config_path, "w") as f:
        toml.dump(user_config, f)


# Make sure all deprecation warnings are shown
# See https://docs.python.org/3/library/warnings.html#overriding-the-default-filter
warnings.filterwarnings(
    "default",
    category=DeprecationWarning,
    module="byterover",
)