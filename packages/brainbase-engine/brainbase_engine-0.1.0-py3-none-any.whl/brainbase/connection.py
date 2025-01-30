import json
import websocket
import threading
from typing import Callable, Optional, Dict, Any, List
from .exceptions import ConnectionError


class Connection:
    """
    Manages the WebSocket connection to a Brainbase worker.

    Args:
        api_key (str): The Brainbase API key
        flow_id (str): The ID of the flow
        base_url (str): The base WebSocket URL

    Example:
        >>> connection = worker.run()
        >>> connection.on("message", lambda data: print(data))
    """

    def __init__(self, api_key: str, flow_id: str, base_url: str):
        self.api_key = api_key
        self.flow_id = flow_id
        self.base_url = base_url
        self.ws: Optional[websocket.WebSocketApp] = None
        self.handlers: Dict[str, List[Callable]] = {
            "message": [],
            "error": [],
            "close": [],
        }
        # Add SSL options
        self.ssl_opts = {
            "cert_reqs": 2,  # ssl.CERT_REQUIRED
            "check_hostname": True
        }

    def connect(
        self,
        streaming: bool = True,
        monitor: bool = True,
        functions: List[Dict[str, Any]] = None,
        verify_ssl: bool = True,
    ) -> None:
        """
        Establish the WebSocket connection.

        Args:
            streaming (bool): Enable message streaming
            monitor (bool): Enable connection monitoring
            functions (List[Dict[str, Any]]): List of function definitions
            verify_ssl (bool): Whether to verify SSL certificates
        """
        url = f"{self.base_url}/{self.flow_id}?apiKey={self.api_key}"

        print("Connecting to url", url)

        # Update SSL options based on verify_ssl parameter
        if not verify_ssl:
            self.ssl_opts = {
                "cert_reqs": 0,  # ssl.CERT_NONE
                "check_hostname": False
            }

        def on_message(ws, message):
            if not message.strip():
                return

            if message == "[DONE]":
                return

            try:
                data = json.loads(message)
                # Handle streaming messages
                if isinstance(data, dict) and data.get("type") == "stream":
                    for handler in self.handlers["message"]:
                        handler(data, ws)
                else:
                    # Handle other message types
                    for handler in self.handlers["message"]:
                        handler(data, ws)
            except json.JSONDecodeError:
                # Handle plain text messages
                for handler in self.handlers["message"]:
                    handler({"type": "text", "content": message}, ws)

        def on_error(ws, error):
            for handler in self.handlers["error"]:
                handler(error, ws)

        def on_close(ws, close_status_code, close_msg):
            for handler in self.handlers["close"]:
                handler(ws)

        def on_open(ws):
            init_message = {
                "action": "initialize",
                "data": json.dumps(
                    {
                        "monitor": monitor,
                        "streaming": streaming,
                        "functions": functions or [],
                    }
                ),
            }
            ws.send(json.dumps(init_message))

        self.ws = websocket.WebSocketApp(
            url,
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
        )

        # Run the WebSocket connection in a separate thread with SSL options
        self.ws_thread = threading.Thread(
            target=lambda: self.ws.run_forever(sslopt=self.ssl_opts)
        )
        self.ws_thread.daemon = True
        self.ws_thread.start()

    def on(self, event: str, handler: Callable) -> None:
        """
        Register an event handler.

        Args:
            event (str): Event type ("message", "error", or "close")
            handler (Callable): The handler function that takes (data, websocket) for messages,
                              (error, websocket) for errors, or (websocket) for close events

        Example:
            >>> def handle_message(data, ws):
            ...     print(data)
            >>> connection.on("message", handle_message)
        """
        if event not in self.handlers:
            raise ValueError(f"Unknown event type: {event}")
        self.handlers[event].append(handler)

    def send(self, message: str) -> None:
        """
        Send a message through the WebSocket connection.

        Args:
            message (str): The message to send

        Raises:
            ConnectionError: If the connection is not established
        """
        if not self.ws:
            raise ConnectionError("Connection not established")

        self.ws.send(
            json.dumps(
                {"action": "stream", "data": {"message": message, "streaming": True}}
            )
        )

    def close(self) -> None:
        """Close the WebSocket connection."""
        if self.ws:
            self.ws.close()
