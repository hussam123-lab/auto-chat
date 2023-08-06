import asyncio
import websockets
PORT = 8000
HEADER = 64
import aioconsole

DISCONNECT_MESSAGE = "!DISCONNECT"

SERVER = "localhost"
ADDR = (SERVER,PORT)

async def receive_messages(websocket):
    try:
        while True:
            message = await websocket.recv()
            print(f"Received message: {message}")
    except websockets.exceptions.ConnectionClosedOK:
        print("WebSocket connection closed.")

async def listen():
    async with websockets.connect(f"ws://{SERVER}:{PORT}") as websocket:
        room_number = input("please enter room number you would like to join: ")
        await websocket.send("ROOM:::" + room_number)
        asyncio.create_task(receive_messages(websocket))
        while True:
            # msg = await websocket.recv()
            # print(f"Message revieved: {msg}")
            user_input = await aioconsole.ainput("Please enter a message: ")
            user_input = "MSG:::" + user_input
            print(user_input)
            await websocket.send(user_input)

 
asyncio.get_event_loop().run_until_complete(listen())