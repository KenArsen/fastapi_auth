from fastapi import Response
from src.core.config import settings
from typing import Optional


def set_access_token_cookie(
    response: Response, token: str, max_age: Optional[int] = None
) -> None:
    response.set_cookie(
        key=settings.JWT_ACCESS_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        max_age=max_age or settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


def clear_access_token_cookie(response: Response) -> None:
    response.delete_cookie(
        key=settings.JWT_ACCESS_COOKIE_NAME,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
    )
