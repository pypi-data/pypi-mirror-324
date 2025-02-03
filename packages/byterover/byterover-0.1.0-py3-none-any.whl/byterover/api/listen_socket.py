import sys
import socketio
import typer

class ByteroverSocketClient:
    def __init__(
        self,
        *,
        socket_url: str,
        public_token: str,
        secret_token: str,
        connection_id: str,
        conversation_id: str,
        quiet: bool = False,
        detach: bool = False,
    ):
        self.socket_url = socket_url
        self.public_token = public_token
        self.secret_token = secret_token
        self.connection_id = connection_id
        self.conversation_id = conversation_id
        self.quiet = quiet
        self.detach = detach

        # The server only needs connection_id & conversation_id from query params for the "connect" event
        query = f"?connection_id={self.connection_id}&conversation_id={self.conversation_id}"
        self._full_url = f"{self.socket_url}/socket.io/{query}"

        # We set up the python-socketio AsyncClient
        self.sio = socketio.AsyncClient(logger=not self.quiet, engineio_logger=not self.quiet)
        self._register_event_handlers()

    def _register_event_handlers(self):
        @self.sio.event
        async def connect():
            # This is triggered once the server authenticates us in 'connect' event
            if not self.quiet:
                typer.echo("Connected to Byterover socket.")

            # Now that we're connected, we immediately send the 'sg_note' event
            # Because your server method signature is: sg_note(connection_id, conversation_id, data)
            # we pass them as three arguments in that order:
            # Construct a single dictionary for the second argument
            payload = {
                "connection_id": self.connection_id,
                "conversation_id": self.conversation_id,
                "data": {
                    "action": "message",
                    "args": {"content": "write a bash script that prints hello"}
                },
            }
            if not self.quiet:
                typer.echo(f"Emitting sg_note => {payload}")
            await self.sio.emit("sg_note", payload)

        @self.sio.event
        async def sg_event(data):
            """
            The server may emit 'sg_event' with various messages, e.g. 'auth_ok', or
            error messages, or progress logs. We'll print them if quiet=False.
            """
            if not self.quiet:
                typer.echo(f"[Byterover => sg_event] {data}")

        @self.sio.event
        async def connect_error(data):
            """
            The client fails to connect.
            """
            typer.echo(f"Connect error: {data}")

        @self.sio.event
        async def disconnect(reason=None):
            """
            The server forcibly disconnects or the client closes. We handle it here.
            """
            if not self.quiet:
                typer.echo(f"Disconnected from Byterover socket. reason={reason}")

            # If we're not in 'detach' mode, we exit the script
            if not self.detach:
                typer.echo("Local process died / disconnected; stopping app.")
                await self.disconnect_from_server()
                sys.exit(0)

    async def connect_to_server(self):
        """
        Connects to the Socket.IO server with the given public/secret token as 'auth'.
        """
        try:
            await self.sio.connect(
                self._full_url,
                auth={"public_key": self.public_token, "secret_key": self.secret_token},
                wait_timeout=300,  # allow up to 5 minutes if the server is slow to respond
            )
        except Exception as e:
            typer.echo(f"Error connecting to socket: {e}")
            raise typer.Exit(1)

    async def disconnect_from_server(self):
        """
        Allows manually disconnecting from the socket if desired.
        """
        await self.sio.disconnect()

    async def wait_for_disconnection(self):
        """
        Blocks until the server forcibly disconnects or the user hits Ctrl+C.
        If we do a single-turn approach, the server likely calls 'disconnect()'
        after finishing the 'sg_note' operation.
        """
        await self.sio.wait()