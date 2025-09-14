from typing import List, TYPE_CHECKING
from fastapi import Depends

from src.api.deps import CurrentUserDep
from src.core.exceptions import ForbiddenException

if TYPE_CHECKING:
    from src.models.user import Account
    from src.models.enam import Role


def require_roles(*roles: Role):
    def wrapper(user: Account = Depends(CurrentUserDep)):
        if user.role not in roles:
            raise ForbiddenException(f"User must have one of roles: {roles}")
        return user

    return wrapper


def check_role(user: Account, allowed_roles: List[Role]):
    if user.role not in allowed_roles:
        raise ForbiddenException()
