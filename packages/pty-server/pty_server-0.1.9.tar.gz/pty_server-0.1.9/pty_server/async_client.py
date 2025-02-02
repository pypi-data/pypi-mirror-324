import asyncio
import json
import logging
import uuid
import time

import websockets
from websockets import ConnectionClosedOK

# Adjust if needed; or use your existing constant
PORT = 44440
HOST = "127.0.0.1"

logger = logging.getLogger(__name__)

STATUS_COMPLETED = "completed"
STATUS_STREAMING = "streaming"
STATUS_TIMEOUT = "timeout"


class PtyServerResponse:
    def __init__(self, websocket,command_id: str):
        self.command_id = command_id
        self.websocket = websocket
        self.status = None

    async def stream(self, timeout=2):
        while True:
            try:
                data = await asyncio.wait_for(self.websocket.recv(), timeout=timeout)
                if f"Completed {self.command_id}" in data:
                    yield data.replace(f"Completed {self.command_id}", "")  # Remove the command end marker and keep the rest of the data
                    self.status = STATUS_COMPLETED
                    break
                if data:
                    self.status = STATUS_STREAMING
                    yield data
                else:
                    self.status = STATUS_COMPLETED
                    break
            except asyncio.TimeoutError as e:
                self.status = STATUS_TIMEOUT
                break
            except ConnectionClosedOK as e:
                self.status = STATUS_COMPLETED  # This happens when server closes the connection
                break

    async def text(self, timeout=2):
        data = ""
        async for chunk in self.stream(timeout):
            data += chunk
        return data

    def completed(self):
        return self.status == STATUS_COMPLETED

    def timedout(self):
        return self.status == STATUS_TIMEOUT


class AsyncPtyClient:
    def __init__(self, uri: str = f"ws://{HOST}:{PORT}"):
        """
        :param uri: WebSocket server URI.
        """
        self.uri = uri
        self.websocket = None

    async def connect(self, max_wait_time=5):
        """Establish a WebSocket connection to the server."""
        start_time = time.monotonic()
        while True:
            try:
                logger.info(f"Connecting to {self.uri} ...")
                self.websocket = await websockets.connect(self.uri)
                logger.info("Connection established.")
                break
            except Exception as e:
                elapsed = time.monotonic() - start_time
                if elapsed >= max_wait_time:
                    logger.debug("Exceeded maximum wait time. Giving up.")
                    raise Exception("Max wait time exceeded while trying to connect.") from e
                # Wait for 0.1 seconds before trying again.
                await asyncio.sleep(0.1)

    async def disconnect(self):
        """Close the WebSocket connection."""
        if self.websocket:
            await self.websocket.close()
            logger.info("Disconnected from server")
            self.websocket = None

    async def stream_response(self, timeout=2):
        """
        Generator that reads data from the server until no more data arrives
        within the given `timeout`.

        Yields each message received as a decoded string.
        """
        while True:
            try:
                message = await asyncio.wait_for(self.websocket.recv(), timeout=timeout)
                yield message
            except asyncio.TimeoutError:
                # No new messages within `timeout` seconds; stop streaming
                break
            except websockets.ConnectionClosed:
                logger.info("Connection closed by the server.")
                break

    async def send_message(self, message: str):
        """
        Send a message to the server. In WebSockets, messages are just strings
        or bytes — no need to prefix the length.
        """
        if not self.websocket:
            raise ConnectionError("Not connected to the server. Cannot send message.")

        try:
            logger.info(f"Sending: {message}")
            await self.websocket.send(message)
            return True
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False

    async def send_command(self, command: str):
        command_id = str(uuid.uuid4())
        command_directive = {"command": command, "command_id": command_id}
        if await self.send_message(json.dumps(command_directive)):
            return PtyServerResponse(self.websocket, command_id)
        else:
            return None

    async def __aenter__(self):
        """Called when entering the 'async with' block."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        """Called when exiting the 'async with' block."""
        await self.disconnect()


async def main():
    # Create our client pointing to the server’s WebSocket URI
    uri = f"ws://{HOST}:{PORT}"

    async with AsyncPtyClient(uri) as client:
        # Send a simple command to the server
        command = {"command": "pip install pexpect"}
        await client.send_message(json.dumps(command))

        # Optionally, wait a bit before streaming responses (illustrative only)
        # In production, you might handle the response reading more dynamically.
        await asyncio.sleep(2)

        # Stream any pending messages from the server
        async for response in client.stream_response(timeout=2):
            logger.info(f"Received: {response}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
