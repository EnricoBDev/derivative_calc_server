import asyncio
import json
import websockets

from derivative_calculator import calculate_point_of_differentiability

async def derivative_process(websocket):
    # wait for incoming JSON request
    request = await websocket.recv()
    request_dict = json.loads(request)
    response = calculate_point_of_differentiability(request_dict)
    
    # send JSON response
    await websocket.send(response)


async def main():
    async with websockets.serve(derivative_process, "localhost", 8765):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
