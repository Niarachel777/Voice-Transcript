import asyncio
import websockets
import json

async def websocket_handler(websocket, path):
    async for message in websocket:
        print(f"Received: {message}")
        await websocket.send(json.dumps({"transcript": message}))

start_server = websockets.serve(websocket_handler, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
