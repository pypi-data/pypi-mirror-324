import os
from brainbase.client import BrainbaseClient
from brainbase.utils import handle_message, handle_error, print_worker


def main():
    # Initialize with your API key
    api_key = os.getenv("BRAINBASE_API_KEY")
    # Initialize client
    bb = BrainbaseClient(api_key)

    # List workers
    workers = bb.list_workers()

    new_worker1 = bb.create_worker(
        name="My Test Worker",
        flow_code="""
    loop:
        phone_response = talk(f"provide therapy to the user", True, {})
    until "they say they are bored":
        say("say goodbye")
    """,
    )

    # Run the worker
    connection = new_worker1.run(streaming=True)
    # Register handlers
    connection.on("message", handle_message)
    connection.on("error", handle_error)

    # The connection will run in the background
    try:
        while True:
            message = input()
            if message.lower() == "quit":
                break
            connection.send(message)
    finally:
        connection.close()


if __name__ == "__main__":
    main()
