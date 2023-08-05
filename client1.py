import asyncio
import websockets
PORT = 8000
HEADER = 64
DISCONNECT_MESSAGE = "!DISCONNECT"

SERVER = "localhost"
ADDR = (SERVER,PORT)

async def listen():
    async with websockets.connect(f"ws://{SERVER}:{PORT}") as websocket:
        await websocket.send("ROOM 1")
        while True:
            msg = await websocket.recv()
            print(msg)

 
asyncio.get_event_loop().run_until_complete(listen())