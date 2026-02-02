from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    user_name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    user_name: str
    email: str
    access_token: str
    token_type: str = "bearer"
