import asyncio
from skwebsocket import SecureFileSender

server_uri = "ws://192.168.80.76:8080"
file_path = r"D:\Files\Files\Excel\single\100 MB single\Book2.xlsx"

sender = SecureFileSender(server_uri)
asyncio.run(sender.send_file(file_path, num_slices=10))