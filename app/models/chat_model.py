from datetime import datetime, timezone


def chat_message_model(sender_id: str, receiver_id: str, message: str):
    return {
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "message": message,
        "created_at": datetime.now(timezone.utc),
    }
