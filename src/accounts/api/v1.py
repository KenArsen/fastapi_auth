from fastapi import APIRouter, Response

from src.accounts.dependencies import CurrentUserDep
from src.accounts.repositories import AccountRepository
from src.accounts.schemas import TokenOut, MeOut, RegistrationIn, LoginIn
from src.accounts.services import AuthService
from src.core.dependencies import DBSessionDep
from src.accounts.cookies import set_access_token_cookie, clear_access_token_cookie

router = APIRouter(prefix="/auth", tags=["Accounts"])


@router.post("/register/", response_model=MeOut)
async def register(session: DBSessionDep, data: RegistrationIn):
    dao = AccountRepository(session)
    service = AuthService(dao)
    return await service.register(data)


@router.post("/login/", response_model=TokenOut)
async def login(response: Response, session: DBSessionDep, data: LoginIn):
    dao = AccountRepository(session)
    service = AuthService(dao)
    token = await service.login(data)
    set_access_token_cookie(response, token.access_token)
    return token


@router.post("/logout/")
async def logout(response: Response):
    clear_access_token_cookie(response)
    return {"detail": "Successfully logged out"}


@router.get("/me/", response_model=MeOut)
async def me(current_user: CurrentUserDep):
    return current_user
