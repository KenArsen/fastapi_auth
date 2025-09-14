from src.dao.user import AccountDAO
from src.models.user import Account
from src.shemas.auth import AccountCreateShema
from src.shemas.token import TokenShema, TokenDataShema
from src.services.token import TokenService
from src.core.exceptions import UserAlreadyExistsException, InvalidEmailOrPasswordException

class AuthService:
    def __init__(self, dao: AccountDAO):
        self.dao = dao

    async def register(self, data: AccountCreateShema) -> Account:
        existing = await self.dao.get_by_email(data.email)
        if existing:
            raise UserAlreadyExistsException()
        account = Account(**data.model_dump())
        return await self.dao.create(account)

    async def token(self, data: TokenDataShema) -> TokenShema:
        account = await self.dao.get_by_email(data.email)
        if account is None or not account.verify_password(data.password):
            raise InvalidEmailOrPasswordException()
        access_token = TokenService.create_access_token(account)
        return TokenShema(access_token=access_token, token_type="bearer")
