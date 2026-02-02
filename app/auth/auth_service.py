from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.db.database import users_collection
from app.models.user_model import user_model


# -------------------------
# Signup (SERVICE)
# -------------------------
async def signup_user(
    user_name: str,
    email: str,
    password: str,
) -> None:
    try:
        user = await users_collection.find_one({"email": email})
        if user:
            raise Exception("User already exists with this email")

        new_user = user_model(
            user_name=user_name,
            email=email,
            hashed_password=hash_password(password),
        )

        await users_collection.insert_one(new_user)

    except Exception as e:
        raise Exception(str(e))


# -------------------------
# Login (SERVICE)
# -------------------------
async def login_user(email: str, password: str) -> dict:
    try:
        user = await users_collection.find_one({"email": email})
        if not user:
            raise Exception("Email not found")

        if not verify_password(password, user["password"]):
            raise Exception("Invalid password")

        access_token = create_access_token(str(user["_id"]))

        return {
            "id": str(user["_id"]),
            "user_name": user["user_name"],
            "email": user["email"],
            "access_token": access_token,
        }

    except Exception as e:
        raise Exception(str(e))
