from app.chat.batch_writer import ChatBatchWriter
from app.models.chat_model import chat_message_model
from app.socket.manager import ConnectionManager

socket_manager = ConnectionManager()
batch_writer = ChatBatchWriter(batch_size=100, flush_interval=5)


async def broadcast(message: dict):
    sender_id = message["sender_id"]
    receiver_id = message["receiver_id"]
    text = message["message"]

    # print(message["sender_id"])
    # print(message["receiver_id"])
    # print(message["message"])
    await socket_manager.send_to_user(receiver_id, message)
    await socket_manager.send_to_user(sender_id, message)

    chat_doc = chat_message_model(
        sender_id=sender_id,
        receiver_id=receiver_id,
        message=text,
    )
    
    await batch_writer.add(chat_doc)
