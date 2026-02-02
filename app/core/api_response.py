from fastapi import status
from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    statusCode: int
    data: Optional[T] = None
    errors: Optional[Any] = None

    # ---------- SUCCESS ----------
    @classmethod
    def ok(
        cls,
        data: T,
        message: str = "Success",
        statusCode: int = status.HTTP_200_OK,
    ):
        return cls(
            success=True,
            message=message,
            statusCode=statusCode,
            data=data,
        )

    @classmethod
    def created(
        cls,
        data: T,
        message: str = "Resource created",
        statusCode: int = status.HTTP_201_CREATED,
    ):
        return cls(
            success=True,
            message=message,
            statusCode=statusCode,
            data=data,
        )

    # ---------- ERROR ----------
    @classmethod
    def error(
        cls,
        message: str = "Something went wrong",
        statusCode: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        errors: Optional[Any] = None,
    ):
        return cls(
            success=False,
            message=message,
            statusCode=statusCode,
            errors=errors,
        )

    @classmethod
    def bad_request(cls, message: str = "Bad request", errors: Optional[Any] = None):
        return cls.error(message, status.HTTP_400_BAD_REQUEST, errors)

    @classmethod
    def unauthorized(cls, message: str = "Unauthorized"):
        return cls.error(message, status.HTTP_401_UNAUTHORIZED)

    @classmethod
    def forbidden(cls, message: str = "Forbidden"):
        return cls.error(message, status.HTTP_403_FORBIDDEN)

    @classmethod
    def not_found(cls, message: str = "Not found"):
        return cls.error(message, status.HTTP_404_NOT_FOUND)

    @classmethod
    def conflict(cls, message: str = "Conflict"):
        return cls.error(message, status.HTTP_409_CONFLICT)

    @classmethod
    def exception_failed(cls, message: str = "Exception failed", errors: Optional[Any] = None):
        return cls.error(message, status.HTTP_417_EXPECTATION_FAILED, errors)
