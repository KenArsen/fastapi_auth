from typing import Annotated

from fastapi import Depends, Request

from src.accounts.models import Account
from src.accounts.repositories import AccountRepository
from src.accounts.security import decode_access_token
from src.core.config import settings
from src.core.dependencies import SessionDep
from src.core.exceptions import (
    AccessTokenMissingException,
    InvalidTokenException,
    InvalidTokenPayloadException,
    NotFoundException,
)


async def get_current_user(request: Request, session: SessionDep) -> Account:
    token = request.cookies.get(settings.JWT_ACCESS_COOKIE_NAME)
    if not token:
        raise AccessTokenMissingException()

    try:
        payload = decode_access_token(token)
        email: str | None = payload.get("sub")
        if email is None:
            raise InvalidTokenPayloadException()
    except Exception as err:
        raise InvalidTokenException() from err

    dao = AccountRepository(session)
    user = await dao.get_by_email(email=email)
    if not user:
        raise NotFoundException("User")

    return user


CurrentUserDep = Annotated[Account, Depends(get_current_user)]
