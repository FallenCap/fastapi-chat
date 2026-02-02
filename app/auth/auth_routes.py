from fastapi import APIRouter
from app.auth.auth_service import signup_user, login_user
from app.auth.auth_schemas import SignupRequest, LoginRequest
from app.core.api_response import ApiResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


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
            message="User registered successfully",
        )

    except Exception as error:
        return ApiResponse.conflict(
            message="Unable to register user",
        )


@router.post("/login", response_model=ApiResponse[dict])
async def login(payload: LoginRequest):
    try:
        data = await login_user(payload.email, payload.password)

        return ApiResponse.ok(
            data=data,
            message="Login successful",
        )

    except Exception as error:
        return ApiResponse.unauthorized(
            message="Invalid email or password",
        )
