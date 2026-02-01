from fastapi import HTTPException, status

from app.core.security import create_access_token, hash_password, verify_password
from app.db.database import users_collection
from app.models.user_model import user_model


# User Signup
async def signup_user(user_name: str, email: str, password: str):
    existing_user = await users_collection.find_one({"email": email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already registered"
        )

    user = user_model(
        user_name=user_name, email=email, hashed_password=hash_password(password)
    )

    await users_collection.insert_one(user)
    return {"message": "User registered successfully"}


# User Login
async def login_user(email: str, password: str) -> dict:
    user = await users_collection.find_one({"email": email})

    if not user or not verify_password(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    access_token = create_access_token(str(user["_id"]))
    return {"access_token": access_token}
