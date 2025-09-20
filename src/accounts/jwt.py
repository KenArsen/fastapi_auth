from typing import Any, Dict

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from src.core.config import settings
from src.core.exceptions import InvalidTokenException
from src.utils.datetime import get_expiration_time


def create_access_token(subject: str) -> str:
    expire = get_expiration_time(settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    payload: Dict[str, Any] = {
        "sub": subject,
        "exp": expire,
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    return token


def decode_access_token(token: str) -> Dict[str, Any]:
    try:
        payload: Dict[str, Any] = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except ExpiredSignatureError:
        raise InvalidTokenException()
    except InvalidTokenError:
        raise InvalidTokenException()
