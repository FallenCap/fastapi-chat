from app.models.chat_model import chat_message_model
from app.socket.manager import socket_manager
from app.chat.batch_writer import batch_writer


async def broadcast(message: dict):
    sender_id = message["sender_id"]
    receiver_id = message["receiver_id"]
    text = message["message"]

    await socket_manager.send_to_user(receiver_id, message)
    await socket_manager.send_to_user(sender_id, message)

    chat_doc = chat_message_model(
        sender_id=sender_id,
        receiver_id=receiver_id,
        message=text,
    )

    await batch_writer.add(chat_doc)
