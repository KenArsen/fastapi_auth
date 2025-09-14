from sqlalchemy import select
from src.models.user import Account
from src.dao.base import BaseDAO


class AccountDAO(BaseDAO):
    def __init__(self, session):
        super().__init__(Account, session)

    async def get_by_email(self, email: str) -> Account | None:
        result = await self.session.execute(
            select(self.model).where(self.model.email == email)
        )
        return result.scalar_one_or_none()

    async def create(self, account: Account) -> Account:
        account.set_password(account.password)
        return await super().create(account)
