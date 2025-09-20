from src.accounts.models import Account
from src.accounts.repositories import AccountRepository
from src.accounts.schemas import LoginIn, RegistrationIn, TokenOut
from src.accounts.security import create_access_token, hash_password, verify_password
from src.core.exceptions import (
    InvalidEmailOrPasswordException,
    UserAlreadyExistsException,
)


class AuthService:
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    async def register(self, data: RegistrationIn) -> Account:
        existing = await self.repository.get_by_email(data.email)
        if existing:
            raise UserAlreadyExistsException()

        account = Account(**data.model_dump())
        account.password = hash_password(data.password)
        return await self.repository.create(account)

    async def login(self, data: LoginIn) -> TokenOut:
        account = await self.repository.get_by_email(data.email)
        if account is None or not verify_password(data.password, account.password):
            raise InvalidEmailOrPasswordException()

        access_token = create_access_token(subject=account.email)
        return TokenOut(access_token=access_token, token_type="bearer")
