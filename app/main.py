from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.auth.auth_routes import router as auth_router
from app.chat.chat_routes import router as chat_router
from app.core.config import settings
from app.socket.manager import ConnectionManager
from app.db.database import check_connection, client
from app.kafka.consumer import KafkaConsumerService
from app.kafka.producer import start_producer
from app.chat.broadcast_handler import broadcast
from app.chat.batch_writer import ChatBatchWriter

kafka_consumer = KafkaConsumerService()
socket_manager = ConnectionManager()
batch_writer = ChatBatchWriter()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Starting in {settings.ENV} mode")
    try:
        await check_connection()
        await start_producer()
        await kafka_consumer.start(broadcast)
        await batch_writer.start()
    except Exception as e:
        print("Startup Error", e)
        raise

    yield

    await kafka_consumer.stop()
    await batch_writer.stop()
    client.close()


app = FastAPI(lifespan=lifespan)

# Routes
app.include_router(auth_router, prefix="/api/auth")
app.include_router(chat_router, prefix="/ws")
