import json
from datetime import datetime
from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketState


app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def broadcast(self, json_data: str):
        for connection in self.connections:
            await connection.send_json(json_data)

    async def receive_text(self, websocket: WebSocket):
        return (await websocket.receive_text())
        
    async def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

manager = ConnectionManager()

@app.get("/")
async def get():
    html = ""
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    return HTMLResponse(html)

@app.get("/index.js")
async def get():
    js = ""
    with open('index.js', 'r', encoding='utf-8') as f:
        js = f.read()
    return HTMLResponse(js)

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)

    while websocket.client_state != WebSocketState.DISCONNECTED:
        try:
            message_text = (await manager.receive_text(websocket))

            await manager.broadcast({
                "data": {
                    "client": {
                        "id": client_id,
                    },
                    "message": {
                        "text": message_text,
                    },
                }
            })

        except WebSocketDisconnect:
            await manager.disconnect(websocket)