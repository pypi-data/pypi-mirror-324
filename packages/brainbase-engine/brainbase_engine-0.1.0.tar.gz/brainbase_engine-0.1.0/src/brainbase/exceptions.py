"""
Custom exceptions for the Brainbase SDK.
"""


class BrainbaseError(Exception):
    """Base exception for all Brainbase-related errors."""

    pass


class AuthenticationError(BrainbaseError):
    """Raised when there are issues with API authentication."""

    pass


class ConnectionError(BrainbaseError):
    """Raised when there are issues with the WebSocket connection."""

    pass


class StreamError(BrainbaseError):
    """Raised when there are issues with the message stream."""

    pass


class ValidationError(BrainbaseError):
    """Raised when there are issues with parameter validation."""

    pass
