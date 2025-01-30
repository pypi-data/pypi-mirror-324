"""
Brainbase Python SDK
~~~~~~~~~~~~~~~~~~~

A Python SDK for interacting with Brainbase's WebSocket API.

Basic usage:

    >>> from brainbase import BrainbaseEngine
    >>> engine = BrainbaseEngine("your-api-key")
    >>> worker = engine.get_worker("worker-id")
    >>> connection = worker.run()
    >>> connection.on("message", lambda data: print(data))

For more information, see https://github.com/brainbase/brainbase-python
"""
from .connection import Connection
from .exceptions import BrainbaseError, ConnectionError, AuthenticationError

__version__ = "0.1.0"
__all__ = [
    "Connection",
    "BrainbaseError",
    "ConnectionError",
    "AuthenticationError",
]
