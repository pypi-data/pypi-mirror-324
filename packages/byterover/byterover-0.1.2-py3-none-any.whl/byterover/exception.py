class Error(Exception):
    """
    Base class for all Byterover errors.

    """


class RemoteError(Error):
    """Raised when an error occurs on the Byterover server."""


class TimeoutError(Error):
    """Base class for Byterover timeouts."""


class FunctionTimeoutError(TimeoutError):
    """Raised when a Function exceeds its execution duration limit and times out."""


class ConnectionError(Error):
    """Raised when an issue occurs while connecting to the Byterover servers."""


class InvalidError(Error):
    """Raised when user does something invalid."""


class VersionError(Error):
    """Raised when the current client version of Byterover is unsupported."""


class NotFoundError(Error):
    """Raised when a requested resource was not found."""


class ExecutionError(Error):
    """Raised when something unexpected happened during runtime."""


class _CliUserExecutionError(Exception):
    """Raised when a user error occurs during CLI execution.
    """

    def __init__(self, user_source: str):
        # `user_source` should be the filepath for the user code that is the source of the exception.
        # This is used by our exception handler to show the traceback starting from that point.
        self.user_source = user_source

class DeprecationError(UserWarning):
    """UserWarning category emitted when a deprecated feature is used."""

    # Overloading it to evade the default filter, which excludes __main__.


class PendingDeprecationError(UserWarning):
    """Soon to be deprecated feature. Only used intermittently because of multi-repo concerns."""


class ServerWarning(UserWarning):
    """Warning originating from the Byterover server and re-issued in client code."""


class InputCancellation(BaseException):
    """Raised when the current input is cancelled by the task

    Intentionally a BaseException instead of an Exception, so it won't get
    caught by unspecified user exception clauses that might be used for retries and
    other control flow.
    """

class ClientClosed(Error):
    pass

class AuthError(Error):
    """Raised when a client has missing or invalid authentication."""