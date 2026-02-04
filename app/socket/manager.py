from fastapi import WebSocket
from typing import Dict, Set


class ConnectionManager:
    def __init__(self):
        # user_id -> set of sockets
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(user_id, set()).add(websocket)
        print(self.active_connections)

    def disconnect(self, user_id: str, websocket: WebSocket):
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_to_user(self, user_id: str, data: dict):
        
        sockets = self.active_connections.get(user_id, set())
        for ws in sockets:
            await ws.send_json(data)

