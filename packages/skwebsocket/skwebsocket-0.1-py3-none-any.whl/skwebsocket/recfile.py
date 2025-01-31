import asyncio
from skwebsocket import SecureFileReceiver

receiver = SecureFileReceiver(save_directory=r"D:\prath\rec")
asyncio.run(receiver.start_server())