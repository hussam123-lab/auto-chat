import asyncio
 
import websockets
 
# create handler for each connection

connections = {}

rooms = {}

room_inside = {}

async def room_add(websocket,message):
    _, room_id = message.split(":::")

    if websocket.__str__() not in room_inside:
        room_inside[websocket.__str__()] = room_id
    if room_id not in rooms:
        rooms[room_id] = [websocket.__str__()]
    else:
        rooms[room_id].append(websocket.__str__())
    await websocket.send("Connected!")

async def message_room(websocket,message):
    print("message: ",message)
    _, message = message.split(":::")
    room_id = room_inside.get(websocket.__str__())
    connected_clients = rooms.get(room_id)
    for client_name in connected_clients:
        if client_name != websocket.__str__():
            print("client_name: ",client_name)
            client_connection = connections.get(client_name)
            await client_connection.send(message)
        
    

funcs = {
    "ROOM" : room_add,
    "MSG": message_room
    
}

async def message_handler(websocket,message):
    command = message.split(":::")[0]
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
        print(f"Recieved message: {message} from {websocket.__str__()}")
        await message_handler(websocket,message)

 
 
start_server = websockets.serve(handler, "localhost", 8000)
 
print("Server starting and listening...")
 
asyncio.get_event_loop().run_until_complete(start_server)
 
asyncio.get_event_loop().run_forever()