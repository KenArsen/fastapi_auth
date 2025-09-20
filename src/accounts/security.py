from typing import Any, Dict, Optional

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from passlib.context import CryptContext
from fastapi import Response

from src.core.config import settings
from src.core.exceptions import InvalidTokenException
from src.utils.datetime import get_expiration_time

# Контекст для работы с паролями
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# =======================
# Password Hashing
# =======================
def hash_password(password: str) -> str:
    """Хэширование пароля"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка соответствия пароля хэшу"""
    return pwd_context.verify(plain_password, hashed_password)


# =======================
# JWT Helpers
# =======================
def create_access_token(subject: str) -> str:
    """Создание access-токена"""
    expire = get_expiration_time(settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    payload: Dict[str, Any] = {"sub": subject, "exp": expire}

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> Dict[str, Any]:
    """Декодирование и валидация access-токена"""
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except ExpiredSignatureError:
        raise InvalidTokenException()
    except InvalidTokenError:
        raise InvalidTokenException()


# =======================
# Cookies
# =======================
def set_access_token_cookie(
        response: Response, token: str, max_age: Optional[int] = None
) -> None:
    """Записать access-токен в cookie"""
    response.set_cookie(
        key=settings.JWT_ACCESS_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        max_age=max_age or settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


def clear_access_token_cookie(response: Response) -> None:
    """Очистить access-токен из cookie"""
    response.delete_cookie(
        key=settings.JWT_ACCESS_COOKIE_NAME,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
    )
