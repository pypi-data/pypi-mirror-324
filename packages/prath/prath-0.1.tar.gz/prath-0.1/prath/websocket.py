import asyncio
import websockets
import logging
import zlib  # For compression
from cryptography.fernet import Fernet  # For encryption

# Constants
CHUNK_SIZE = 2048  # Define the size of each chunk (in bytes)

logging.basicConfig(level=logging.INFO)


logging.info("WebSocket server starting...")


class WebSocketManager:
    def __init__(self):
        self.clients = {}  # To store the client info (encryption keys)
        self.message_buffers = {}  # Temporary storage for message slices

    async def register(self, websocket):
        self.clients[websocket] = None  # No key assigned yet
        self.message_buffers[websocket] = []  # Buffer for reassembling messages
        logging.info(f"New client connected: {websocket}")

    async def unregister(self, websocket):
        self.clients.pop(websocket, None)
        self.message_buffers.pop(websocket, None)
        logging.info(f"Client disconnected: {websocket}")

    async def handle_message(self, websocket, message):
        # Use the assigned key for decryption
        key = self.clients[websocket]
        if not key:
            logging.warning("No key assigned for this client. Dropping message.")
            return

        cipher_suite = Fernet(key)
        logging.info(f"message---->{message}")
        # Decrypt and decompress the received chunk
        chunk = cipher_suite.decrypt(message)
        decompressed_chunk = zlib.decompress(chunk).decode("utf-8")

        # Handle slicing metadata
        if decompressed_chunk.startswith("END:"):
            # Last slice received, complete the message
            full_message = "".join(self.message_buffers[websocket])
            self.message_buffers[websocket] = []  # Clear the buffer
            logging.info(f"Full reassembled message: {full_message}")

            # Send a compressed and encrypted response
            response_text = f"Server received your message: {full_message}"
            compressed_response = zlib.compress(response_text.encode("utf-8"))
            encrypted_response = cipher_suite.encrypt(compressed_response)
            await websocket.send(encrypted_response)
        else:
            # Add the chunk to the buffer
            self.message_buffers[websocket].append(decompressed_chunk)

    async def handler(self, websocket):
        await self.register(websocket)
        try:
            # Generate and send a new encryption key to the client
            key = Fernet.generate_key()
            self.clients[websocket] = key
            await websocket.send(key)  # Send the dynamic key to the client securely

            # Handle incoming slices
            async for message in websocket:
                await self.handle_message(websocket, message)
        finally:
            await self.unregister(websocket)
            await websocket.close()

class WebSocketServer:
    def __init__(self, host="0.0.0.0", port=8080):
        self.host = host
        self.port = port
        self.manager = WebSocketManager()

    async def start(self):
        server = await websockets.serve(self.manager.handler, self.host, self.port)
        logging.info(f"WebSocket Server started on {self.host}:{self.port}")
        await server.wait_closed()  # Keep the server running

class WebSocketClient:
    def __init__(self, uri):
        self.uri = uri
        self.key = None  # To store the encryption key

    async def receive_key(self, websocket):
        # Receive the encryption key securely from the server
        self.key = await websocket.recv()
        logging.info(f"Received encryption key: {self.key}")

    async def send_message(self, message):
        try:
            async with websockets.connect(self.uri) as websocket:
                logging.info(f"Connected to server at {self.uri}")

                # Receive the encryption key from the server
                await self.receive_key(websocket)

                # Split the message into chunks
                for i in range(0, len(message), CHUNK_SIZE):
                    chunk = message[i:i + CHUNK_SIZE]

                    # Compress the chunk
                    compressed_chunk = zlib.compress(chunk.encode("utf-8"))

                    logging.info(f"Compressed size: {len(compressed_chunk)}")

                    # Encrypt the chunk with the received key
                    cipher_suite = Fernet(self.key)
                    encrypted_chunk = cipher_suite.encrypt(compressed_chunk)

                    logging.info(f"Encrypted size: {len(encrypted_chunk)}")

                    # Send the encrypted and compressed chunk
                    await websocket.send(encrypted_chunk)

                # Mark the end of the message with "END:" keyword
                await websocket.send(cipher_suite.encrypt(zlib.compress("END:".encode("utf-8"))))

                # Wait for the server response
                response = await websocket.recv()
                decrypted_response = cipher_suite.decrypt(response)
                decompressed_response = zlib.decompress(decrypted_response).decode("utf-8")
                logging.info(f"Server response: {decompressed_response}")
        except Exception as e:
            logging.error(f"Error: {e}")
