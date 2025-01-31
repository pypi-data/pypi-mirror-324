import asyncio
import websockets
import logging
import zlib  # For compression
from cryptography.fernet import Fernet  # For encryption
import os
import math
import time

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
    def __init__(self, host="0.0.0.0", port=9090):
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


class SecureFileSender:
    """Handles secure file transfer over WebSockets with encryption and compression."""

    def __init__(self, server_uri):
        self.server_uri = server_uri
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    async def send_file(self, file_path, num_slices=10):
        """Encrypts, compresses, and sends a file to the server."""
        try:
            async with websockets.connect(self.server_uri) as websocket:
                print(f"Connected to {self.server_uri}")

                start_time = time.time()

                # Send encryption key
                await websocket.send(self.key)

                # Send filename
                file_name = os.path.basename(file_path)
                encrypted_filename = self.cipher.encrypt(f"FILENAME:{file_name}".encode())
                await websocket.send(encrypted_filename)

                # Read & compress file
                with open(file_path, "rb") as file:
                    file_data = file.read()
                compressed_data = zlib.compress(file_data)

                total_size = len(compressed_data)
                chunk_size = min(10 * 1024 * 1024, math.ceil(total_size / num_slices))

                print(f"Total file size: {total_size} bytes, Chunk size: {chunk_size} bytes")

                # Send file in chunks
                for i in range(0, total_size, chunk_size):
                    chunk = compressed_data[i:i + chunk_size]
                    encrypted_chunk = self.cipher.encrypt(chunk)
                    await websocket.send(encrypted_chunk)
                    print(f"Sent chunk {i // chunk_size + 1}/{num_slices}")

                    # Periodically send ping to keep connection alive
                    if i % (5 * chunk_size) == 0:
                        await websocket.ping()

                # Send End marker
                encrypted_end_marker = self.cipher.encrypt(b"END:")
                await websocket.send(encrypted_end_marker)
                print("File transfer complete!")

                duration = time.time() - start_time
                print(f"Total transfer time: {duration:.2f} seconds")

        except Exception as e:
            print(f"Error sending file: {e}")


class SecureFileReceiver:
    """Handles secure file reception, decryption, and decompression."""

    def __init__(self, save_directory="received_files/"):
        self.clients = {}  # Stores client encryption keys
        self.file_buffers = {}  # Stores received file chunks
        self.file_names = {}  # Stores filenames
        self.save_directory = save_directory
        os.makedirs(self.save_directory, exist_ok=True)

    async def handle_client(self, websocket):
        """Handles a connected client for receiving files."""
        try:
            # Receive encryption key
            dynamic_key = await websocket.recv()
            cipher = Fernet(dynamic_key)
            self.clients[websocket] = cipher
            self.file_buffers[websocket] = bytearray()

            print(f"Received encryption key from client.")

            # Receive file name
            encrypted_filename = await websocket.recv()
            self.file_names[websocket] = cipher.decrypt(encrypted_filename).decode().replace("FILENAME:", "")
            print(f"Receiving file: {self.file_names[websocket]}")

            # Receive file chunks
            async for message in websocket:
                decrypted_message = cipher.decrypt(message)
                if decrypted_message == b"END:":
                    file_name = self.file_names[websocket]
                    file_path = os.path.join(self.save_directory, file_name)

                    # Decompress & Save
                    decompressed_data = zlib.decompress(self.file_buffers[websocket])
                    with open(file_path, "wb") as file:
                        file.write(decompressed_data)

                    print(f"File saved as: {file_path}")

                    # Cleanup
                    del self.file_buffers[websocket]
                    del self.file_names[websocket]
                    break
                else:
                    self.file_buffers[websocket].extend(decrypted_message)

        except Exception as e:
            print(f"Error receiving file: {e}")

    async def start_server(self, host="0.0.0.0", port=8080):
        """Starts the WebSocket server to receive files."""
        async with websockets.serve(self.handle_client, host, port, max_size=None, ping_interval=30, ping_timeout=60):
            print(f"Server running on {host}:{port}")
            await asyncio.Future()  # Keep running



