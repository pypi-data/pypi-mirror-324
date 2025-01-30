"""
Utility functions for the Brainbase Python SDK.
"""
import os

def get_api_url():
    return "http://localhost:3000" if os.getenv("USE_DEVELOPMENT") == "True" else "https://brainbase-monorepo-api.onrender.com"

def get_ws_url():
    return "ws://localhost:7001" if os.getenv("USE_DEVELOPMENT") == "True" else "wss://brainbase-realtime-engine.onrender.com"


def handle_message(data, ws):
    if isinstance(data, dict):
        if data.get("type") == "stream":
            print(data.get("content"), end="", flush=True)
            # Add a newline if the content ends with punctuation
            if data.get("content", "").strip().endswith((".", "?", "!")):
                print("\n")
        elif data.get("type") == "function_call":
            print(f"\nSystem: Function called - {data.get('function')}\n")
        elif data.get("action") == "done":
            print("\nSystem: Conversation complete\n")
            ws.close()
        else:
            print(f"\nSystem message: {data}\n")
    else:
        print(f"\nReceived: {data}\n")


def handle_error(error, ws):
    print(f"Error: {error}")

