#import asyncwebsockets

import asyncio
import websockets

async def hello():
    async with websockets.connect('ws://localhost:5678') as websocket:
        while True:
            greeting = await websocket.recv()
            print("< {}".format(greeting))

asyncio.get_event_loop().run_until_complete(hello())
# trio.run(hello)

