from fastapi import Response
from src.core.config import settings


def set_access_token_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=settings.JWT_ACCESS_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        max_age=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


def clear_access_token_cookie(response: Response) -> None:
    response.delete_cookie(settings.JWT_ACCESS_COOKIE_NAME)
