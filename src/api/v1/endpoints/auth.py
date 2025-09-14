from fastapi import APIRouter
from src.core.deps import SessionDep
from src.dao.user import AccountDAO
from src.services.auth import AuthService
from src.shemas.auth import AccountCreateShema
from src.shemas.token import TokenDataShema, TokenShema
from src.shemas.auth import AccountReadShema

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register/", response_model=AccountReadShema)
async def register(session: SessionDep, data: AccountCreateShema):
    dao = AccountDAO(session)
    service = AuthService(dao)
    return await service.register(data)


@router.post("/token/", response_model=TokenShema)
async def token(session: SessionDep, data: TokenDataShema):
    dao = AccountDAO(session)
    service = AuthService(dao)
    return await service.token(data)
