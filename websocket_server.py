import asyncio
import websockets
import json
from pynput.keyboard import Key, Controller

keyboard = Controller()

async def handle_connection(websocket, path):
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                print(f"Received message: {data}")
                if data['type'] == 'keypress':
                    simulate_key_press(data['key'])
                else:
                    print(f"Received unknown message type: {data['type']}")
            except json.JSONDecodeError:
                print(f"Received invalid JSON: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed")
    except Exception as e:
        print(f"Error handling connection: {e}")


def simulate_key_press(key):
    numpad_keys = {
        "0": "0",
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
        ".": ".",
        "/": "/",
        "*": "*",
        "-": "-",
        "+": "+",
        "Enter": Key.enter
    }
    
    if key in numpad_keys:
        keyboard.press(numpad_keys[key])
        keyboard.release(numpad_keys[key])
        print(f"Simulated key press: {key}")
    else:
        print(f"Received unknown key: {key}")
   
  
async def main():
    async with websockets.serve(handle_connection, "0.0.0.0", 8765):
        print("WebSocket server started on ws://0.0.0.0:8765")
        await asyncio.Future()
        
if __name__ == "__main__":
    asyncio.run(main())
