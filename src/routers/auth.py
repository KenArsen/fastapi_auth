import logging
from fastapi import APIRouter, status

from src.core.deps import SessionDep
from src.shemas.auth import AccountCreateShema, AccountReadShema
from src.services.auth import AuthService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register/",
    status_code=status.HTTP_201_CREATED,
    response_model=AccountReadShema,
)
async def register(session: SessionDep, data: AccountCreateShema):
    logger.info(f"{data=}")
    service = AuthService(session=session)
    return await service.register(data=data)
