from byterover.cli.entry_point import entrypoint_cli
from byterover.config import config
from byterover.exception import _CliUserExecutionError
from byterover.cli._traceback import highlight_byterover_deprecation_warnings


def main():
    highlight_byterover_deprecation_warnings()

    try:
        entrypoint_cli()

    except _CliUserExecutionError as exc:
        if config.get("traceback"):
            raise

if __name__ == "__main__":
    main()