from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import Account
from src.shemas.auth import AccountCreateShema
from src.crud.user import AccountCRUD


class AuthService:
    def __init__(
        self, session: AsyncSession, crud: AccountCRUD = AccountCRUD()
    ) -> None:
        self.session = session
        self.crud = crud

    async def register(self, data: AccountCreateShema) -> Account:
        account = Account(**data.model_dump())
        account = await self.crud.create(session=self.session, account=account)
        return account
