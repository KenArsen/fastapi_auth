from fastapi import APIRouter, Response
from src.dependencies.dao_dep import SessionDep
from src.dependencies.auth_dep import CurrentUserDep
from src.dao.user import AccountDAO
from src.services.auth import AuthService
from src.shemas.auth import AccountCreateShema, AccountLoginShema, AccountReadShema
from src.shemas.token import TokenShema
from src.utils.cookie_helpers import set_access_token_cookie, clear_access_token_cookie

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register/", response_model=AccountReadShema)
async def register(session: SessionDep, data: AccountCreateShema):
    dao = AccountDAO(session)
    service = AuthService(dao)
    return await service.register(data)


@router.post("/login/", response_model=TokenShema)
async def login(response: Response, session: SessionDep, data: AccountLoginShema):
    dao = AccountDAO(session)
    service = AuthService(dao)
    token = await service.login(data)
    set_access_token_cookie(response, token.access_token)
    return token


@router.post("/logout/")
async def logout(response: Response):
    clear_access_token_cookie(response)
    return {"detail": "Successfully logged out"}


@router.get("/me/", response_model=AccountReadShema)
async def me(current_user: CurrentUserDep):
    return current_user
