import jwt
from typing import Any
from datetime import datetime, timedelta, timezone
from src.core.config import settings
from src.models.user import Account


class TokenService:
    secret_key =  settings.JWT_SECRET_KEY
    algorithm =  settings.JWT_ALGORITHM
    expire_minutes = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES

    @classmethod
    def create_access_token(cls, account: Account):
        expire = datetime.now(timezone.utc) + timedelta(minutes=cls.expire_minutes)
        payload: dict[str, Any] = {
            "sub": account.email,
            "exp": expire,
        }

        return jwt.encode(payload, cls.secret_key, algorithm=cls.algorithm)
