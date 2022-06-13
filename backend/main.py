from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import json
from time import sleep
app = FastAPI()

@app.websocket("/netview-ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # sleep(2)
        data = await websocket.receive_text()
        print(data)
        if data :
            values = {"hosts":[
                "192.168.14.32",
                "192.168.14.45",
                "192.168.14.22",
                "8.8.8.8",
                "1.1.1.1",
                "142.251.37.174",
                "98.137.11.164"
                ],
                "connections":[
                    "192.168.14.32-8.8.8.8",
                    "192.168.14.45-192.168.14.22",
                    "192.168.14.45-8.8.8.8",
                    "192.168.14.22-1.1.1.1",
                    "192.168.14.22-142.251.37.174",
                    "192.168.14.32-142.251.37.174",
                    "192.168.14.45-98.137.11.164",
                    ]
                }
            await websocket.send_text(json.dumps(values))

