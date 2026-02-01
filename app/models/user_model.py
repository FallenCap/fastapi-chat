from datetime import datetime, timezone


def user_model(user_name: str, email: str, hashed_password: str) -> dict:
    return {
        "user_name": user_name,
        "email": email,
        "password": hashed_password,
        "is_active": True,
        "created_at": datetime.now(timezone.utc),
    }
