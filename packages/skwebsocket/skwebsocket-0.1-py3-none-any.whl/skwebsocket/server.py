from skwebsocket import WebSocketServer
import asyncio


async def main():
    server = WebSocketServer(host="192.168.80.76", port=9090)
    #server = wsabc.WebSocketServer(host="127.0.0.1", port=8765)

    await server.start()  # Starts the WebSocket server asynchronously

if __name__ == "__main__":
    asyncio.run(main())  # Run the async main function