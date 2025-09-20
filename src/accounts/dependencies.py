from typing import Annotated

from fastapi import Depends, Request

from src.core.config import settings
from src.core.dependencies import DBSessionDep
from src.core.exceptions import (
    InvalidTokenPayloadException,
    InvalidTokenException,
    NotFoundException,
    AccessTokenMissingException,
)
from src.accounts.repositories import AccountRepository
from src.accounts.models import Account
from src.accounts.jwt import decode_access_token


async def get_current_user(request: Request, session: DBSessionDep) -> Account:
    token = request.cookies.get(settings.JWT_ACCESS_COOKIE_NAME)
    if not token:
        raise AccessTokenMissingException()

    try:
        payload = decode_access_token(token)
        email: str | None = payload.get("sub")
        if email is None:
            raise InvalidTokenPayloadException()
    except Exception:
        raise InvalidTokenException()

    dao = AccountRepository(session)
    user = await dao.get_by_email(email=email)
    if not user:
        raise NotFoundException("User")

    return user


CurrentUserDep = Annotated[Account, Depends(get_current_user)]
