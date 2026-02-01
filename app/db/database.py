from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings

if settings.MONGO_URI is None or settings.DB_NAME is None:
    raise RuntimeError("DB ENV must be set in the configuration.")


client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.DB_NAME]
users_collection = db.users


async def check_connection() -> None:
    """Check the connection to the MongoDB server."""
    await client.admin.command("ping")
    await users_collection.create_index("email", unique=True)
