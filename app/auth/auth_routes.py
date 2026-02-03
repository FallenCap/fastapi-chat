from fastapi import APIRouter
from app.auth.auth_service import signup_user, login_user
from app.auth.auth_schemas import SignupRequest, LoginRequest
from app.core.api_response import ApiResponse
from app.auth.auth_exceptions import (
    EmailAlreadyExists,
    EmailNotFound,
    InvalidPassword,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


# -------------------------
# Signup (ROUTES)
# -------------------------
@router.post("/signup", response_model=ApiResponse[None])
async def signup(payload: SignupRequest):
    try:
        await signup_user(
            payload.user_name,
            payload.email,
            payload.password,
        )
        return ApiResponse.created(
            data=None,
            message="User registered successfully.",
        )
    except EmailAlreadyExists:
        return ApiResponse.conflict(
            message="Email already exists!",
        )
    except Exception as error:
        return ApiResponse.exception_failed(
            message="Error while signup!",
            errors=str(error),
        )


# -------------------------
# Login (ROUTES)
# -------------------------
@router.post("/login", response_model=ApiResponse[dict])
async def login(payload: LoginRequest):
    try:
        data = await login_user(payload.email, payload.password)

        return ApiResponse.ok(
            data=data,
            message="Login successful",
        )
    except (EmailNotFound, InvalidPassword):
        return ApiResponse.not_found(
            message="Invalid email or password!",
        )
    except Exception as error:
        return ApiResponse.exception_failed(
            message="Error while login!",
            errors=str(error),
        )
