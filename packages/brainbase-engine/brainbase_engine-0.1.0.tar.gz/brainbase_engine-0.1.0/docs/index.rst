Brainbase Python SDK Documentation
================================

The official Python SDK for Brainbase's WebSocket API.

Installation
-----------

.. code-block:: bash

   pip install brainbase

Quick Start
----------

.. code-block:: python

   from brainbase import BrainbaseEngine

   def handle_message(data):
       print(f"Received: {data}")

   # Initialize the engine with your API key
   engine = BrainbaseEngine("your-api-key")

   # Get a worker instance
   worker = engine.get_worker("worker-id")

   # Establish connection
   connection = worker.run(streaming=True)

   # Register message handler
   connection.on("message", handle_message)

   # Send a message
   connection.send("Hello, Brainbase!")

API Reference
------------

.. toctree::
   :maxdepth: 2

   api 