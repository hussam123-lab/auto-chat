import asyncio
 
import websockets
 
# create handler for each connection

connections = {}

rooms = {} # id, [client1,client2.....]

async def room_add(websocket,message):
    _, room_id = message.split(" ")
    if room_id not in rooms:
        rooms[room_id] = [websocket.__str__()]
    else:
        rooms[room_id].append(websocket.__str__())

async def message_room(websocket,message):
    _, message, room_id = message.split(" ")
    print("here")
    connected_clients = rooms.get(room_id)
    for client_name in connected_clients:
        client_connection = connections.get(client_name)
        print(client_connection)
        await client_connection.send(message)
        
    

funcs = {
    "ROOM" : room_add,
    "MSG": message_room
    
}


async def message_handler(websocket,message):
    command = message.split(" ")[0]
    print(message,command)
    command_function = funcs.get(command)
    if command_function:
        await command_function(websocket, message)
    else:
        print(f"Unknown command: {command}")
        

async def handler(websocket, path):
    print(f"Client connected {websocket.__str__()}")
    if websocket.__str__() not in connections:
        connections[websocket.__str__()] = websocket
    async for message in websocket:
        await message_handler(websocket,message)
        

        print(f"Recieved message: {message}")
        print(rooms)
        await websocket.send("pong")

 
 
start_server = websockets.serve(handler, "localhost", 8000)
 
print("Server starting and listening...")
 
asyncio.get_event_loop().run_until_complete(start_server)
 
asyncio.get_event_loop().run_forever()