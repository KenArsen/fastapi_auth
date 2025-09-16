from src.dao.user import AccountDAO
from src.models.user import Account
from src.schemas.auth import AccountCreateSchema, AccountLoginSchema
from src.schemas.token import TokenSchema
from src.core.exceptions import (
    UserAlreadyExistsException,
    InvalidEmailOrPasswordException,
)
from src.utils.hashing_helpers import verify_password, hash_password
from src.utils.jwt_helpers import create_access_token


class AuthService:
    def __init__(self, dao: AccountDAO):
        self.dao = dao

    async def register(self, data: AccountCreateSchema) -> Account:
        existing = await self.dao.get_by_email(data.email)
        if existing:
            raise UserAlreadyExistsException()

        account = Account(**data.model_dump())
        account.password = hash_password(account.password)

        return await self.dao.create(account)

    async def login(self, data: AccountLoginSchema) -> TokenSchema:
        account = await self.dao.get_by_email(data.email)
        if account is None or not verify_password(data.password, account.password):
            raise InvalidEmailOrPasswordException()

        access_token = create_access_token(subject=account.email)
        return TokenShema(access_token=access_token, token_type="bearer")
