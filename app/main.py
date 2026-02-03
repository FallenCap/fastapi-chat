from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.auth.auth_routes import router as auth_router
from app.core.config import settings
from app.socket.manager import ConnectionManager
from app.db.database import check_connection, client
from app.kafka.consumer import KafkaConsumerService

kafka_consumer = KafkaConsumerService()
socket_manager = ConnectionManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Starting in {settings.ENV} mode")
    try:
        await check_connection()
        print("MongoDB connected")
        await kafka_consumer.start(socket_manager.broadcast)
    except Exception as e:
        print("Startup Error", e)
        raise

    yield

    client.close()
    await kafka_consumer.stop()


app = FastAPI(lifespan=lifespan)

# Routes
app.include_router(auth_router, prefix="/api/auth")
