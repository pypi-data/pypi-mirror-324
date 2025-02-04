"""Helper functions related to displaying tracebacks in the CLI."""
import re
import warnings

from rich.console import Console
from rich.panel import Panel

from ..exception import DeprecationError, PendingDeprecationError, ServerWarning

def highlight_byterover_deprecation_warnings() -> None:
    """Patch the warnings module to make client deprecation warnings more salient in the CLI."""
    base_showwarning = warnings.showwarning

    def showwarning(warning, category, filename, lineno):
        if issubclass(category, (DeprecationError, PendingDeprecationError, ServerWarning)):
            content = str(warning)
            if re.match(r"^\d{4}-\d{2}-\d{2}", content):
                date = content[:10]
                message = content[11:].strip()
            else:
                date = ""
                message = content
            try:
                with open(filename, encoding="utf-8", errors="replace") as code_file:
                    source = code_file.readlines()[lineno - 1].strip()
                message = f"{message}\n\nSource: {filename}:{lineno}\n  {source}"
            except OSError:
                # e.g., when filename is "<unknown>"; raises FileNotFoundError on posix but OSError on windows
                pass
            if issubclass(category, ServerWarning):
                title = "Byterover Warning"
            else:
                title = "Byterover Deprecation Warning"
            if date:
                title += f" ({date})"
            panel = Panel(
                message,
                border_style="yellow",
                title=title,
                title_align="left",
            )
            Console().print(panel)
        else:
            base_showwarning(warning, category, filename, lineno, file=None, line=None)

    warnings.showwarning = showwarning
