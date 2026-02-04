from fastapi import WebSocket, status
from jose import jwt, JWTError
from app.core.config import settings


async def get_current_user_ws(websocket: WebSocket) -> str:
    if not settings.JWT_SECRET or not settings.JWT_ALGORITHM:
        raise RuntimeError("JWT settings are not properly configured.")

    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise RuntimeError("Missing token")

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload["sub"]
    except JWTError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise RuntimeError("Invalid token")
