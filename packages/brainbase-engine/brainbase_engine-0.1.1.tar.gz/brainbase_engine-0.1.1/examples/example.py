import os
from brainbase.client import BrainbaseClient
from brainbase.utils import handle_message, handle_error


def main():
    # Initialize with your API key
    api_key = os.getenv("BRAINBASE_API_KEY")
    # Initialize client
    bb = BrainbaseClient(api_key)

    # # List workers
    # workers = bb.list_workers()

    worker1 = bb.create_worker(
        name="My Test Worker",
        flow_code="""
    state = {}
    meta_prompt = "You're an assistant that helps the user book shifts."
    # Test default model (gpt-4o)
    say("Introduce yourself and mention which AI model you are.")
    
    loop:
        phone_response = talk(f"{meta_prompt} Gather the user's phone number, full name, and facility name. Confirm them as well. if you already have the information, just confirm it.", True, {"phone_number": "+16179011508", "full_name": "John Doe"})
    until "User has given phone number, full name, and facility name and confirmed them":
        print("phone_response")
        print(phone_response)
        say(f"Okay, you're facility is booked. their appoint id is {phone_response}")

        res = "Matt works at Brainbase".ask(question="Where does Matt work? Also, what AI model are you? provide concise answers")
        print(res)

    """,
    )
    
    # worker1 = bb.read_worker("worker_e321de2e-ad50-4c38-ab3f-2c95f35c9a3e")
    
    # Run the worker
    connection = worker1.run(verify_ssl=False)
    print()
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
