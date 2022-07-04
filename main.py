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

        print(self.connections)
        
        for connection in self.connections:
            if connection.client_state == WebSocketState.DISCONNECTED:
                await self.disconnect(connection)

        print("\033[43mCONNECT\033[0m:", self.connections)

    async def broadcast(self, json_data: str):
        for connection in self.connections:
            # try:
            await connection.send_json(json_data)
            # except WebSocketDisconnect:
            #     await self.disconnect(connection)
            #     print(self.connections)
            # except RuntimeError:
            #     await self.disconnect(connection)
            #     print("RUNTIME_ERROR", "|", connection, "|", self.connections)

    async def receive_text(self, websocket: WebSocket):
        return (await websocket.receive_text())
        
    async def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)
        print("\033[31mDISCONNECT\033[0m:", self.connections)

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
    while True:
        try:
            message_text = (await manager.receive_text(websocket))
        except WebSocketDisconnect:
            return 0

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
