from fastapi import HTTPException, status

from src.accounts.dependencies import CurrentUserDep
from src.accounts.enums import Role


async def require_manager(user: CurrentUserDep):
    if user.role != Role.USER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Managers only."
        )
