from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.auth.auth_routes import router as auth_router
from app.core.config import settings
from app.db.database import check_connection, client


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Starting in {settings.ENV} mode")
    try:
        await check_connection()
        print("MongoDB connected")
    except Exception as e:
        print("MongoDB connection failed:", e)
        raise

    yield

    client.close()


app = FastAPI(lifespan=lifespan)

# Routes
app.include_router(auth_router, prefix="/api/auth")
