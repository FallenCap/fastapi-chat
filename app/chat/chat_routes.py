from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.socket.manager import ConnectionManager
from app.socket.dependency import get_current_user_ws
from app.kafka.producer import publish_chat_message

router = APIRouter()
socket_manager = ConnectionManager()


@router.websocket("/chat")
async def chat_ws(ws: WebSocket):
    user_id = await get_current_user_ws(ws)
    await socket_manager.connect(user_id, ws)

    try:
        while True: 
            data = await ws.receive_json()
            await publish_chat_message({
                "sender_id": user_id,
                "receiver_id": data["to"],
                "message": data["message"],
            })
    except WebSocketDisconnect:
        socket_manager.disconnect(user_id, ws)
    