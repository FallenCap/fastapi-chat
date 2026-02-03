from app.auth.auth_exceptions import EmailAlreadyExists, EmailNotFound, InvalidPassword
from app.core.security import create_access_token, hash_password, verify_password
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
    user = await users_collection.find_one({"email": email})
    if user:
        raise EmailAlreadyExists()

    new_user = user_model(
        user_name=user_name,
        email=email,
        hashed_password=hash_password(password),
    )

    await users_collection.insert_one(new_user)


# -------------------------
# Login (SERVICE)
# -------------------------
async def login_user(email: str, password: str) -> dict:
    user = await users_collection.find_one({"email": email})
    if not user:
        raise EmailNotFound()

    if not verify_password(password, user["password"]):
        raise InvalidPassword()

    access_token = create_access_token(str(user["_id"]))

    return {
        "id": str(user["_id"]),
        "user_name": user["user_name"],
        "email": user["email"],
        "access_token": access_token,
    }
