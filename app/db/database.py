from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings

if settings.MONGO_URI is None or settings.DB_NAME is None:
    raise RuntimeError("DB ENV must be set in the configuration.")


client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.DB_NAME]
users_collection = db.users
chat_collection = db.chats


# TODO: Check Mongodb Connection
async def check_connection() -> None:
    await client.admin.command("ping")
    await users_collection.create_index("email", unique=True)
    print("✅ MongoDB connected")
