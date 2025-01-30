# Brainbase Python SDK

The official Python SDK for interacting with Brainbase's REST & WebSocket API. This SDK provides a simple and intuitive way to establish real-time connections with Brainbase workers and handle streaming messages.

## Installation

```bash
pip install brainbase
```

## Features

- WebSocket-based real-time communication
- Message streaming support
- Event-driven architecture
- Function calling capabilities
- Connection monitoring
- Error handling

## Quick Start

```python
from brainbase import BrainbaseEngine

# Initialize the engine with your API key
engine = BrainbaseEngine("your-api-key")

# Get a worker instance
worker = engine.get_worker("worker-id")

# Define a message handler
def handle_message(data, ws):
    if isinstance(data, dict) and data.get("type") == "stream":
        print(data.get("content"), end="", flush=True)

# Establish connection
connection = worker.run(streaming=True)

# Register message handler
connection.on("message", handle_message)

# Send a message
connection.send("Hello, Brainbase!")
```

## Documentation

For detailed documentation, visit [https://docs.brainbase.com/python](https://docs.brainbase.com/python)

## API Reference

### BrainbaseEngine

The main class for interacting with Brainbase's API.

```python
engine = BrainbaseEngine(
    api_key="your-api-key",
)
```

### Worker

Represents a Brainbase worker that can establish WebSocket connections.

```python
worker = engine.get_worker("worker-id")
connection = worker.run(
    streaming=True,  # Enable message streaming
    monitor=True,    # Enable connection monitoring
    functions=[]     # Optional function definitions
)
```

### Connection

Manages the WebSocket connection to a Brainbase worker.

```python
# Register event handlers
connection.on("message", handle_message)
connection.on("error", handle_error)
connection.on("close", handle_close)

# Send messages
connection.send("Your message")

# Close connection
connection.close()
```

## Development

To set up the development environment:

1. Clone the repository
2. Install development dependencies:

```bash
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black .
isort .
```

## Requirements

- Python 3.7+
- websocket-client>=1.0.0
- requests>=2.25.0

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

For support, email support@usebrainbase.xyz or create an issue on our [GitHub repository](https://github.com/brainbase/brainbase-python/issues).

```

```
