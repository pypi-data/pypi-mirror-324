import asyncio
from websocket import WebSocketServer, WebSocketClient

async def run_test():
    # Start WebSocket Server
    server = WebSocketServer()
    server_task = asyncio.create_task(server.start())

    # Wait a bit for the server to start
    await asyncio.sleep(1)

    # Start WebSocket Client and send a message
    client = WebSocketClient("ws://localhost:8080")
    await client.send_message("Hello")

    # Allow some time for communication before shutting down
    await asyncio.sleep(5)

# Run the test
asyncio.run(run_test())
