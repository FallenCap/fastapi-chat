from fastapi import APIRouter

from app.auth.auth_schemas import LoginRequest, SignupRequest, TokenResponse
from app.auth.auth_service import login_user, signup_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
async def signup(payload: SignupRequest):
    return await signup_user(payload.user_name, payload.email, payload.password)


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest):
    return await login_user(payload.email, payload.password)
