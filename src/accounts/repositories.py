from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.accounts.models import Account
from src.core.repositories import BaseRepository


class AccountRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(Account, session)

    async def get_by_email(self, email: str) -> Account | None:
        result = await self.session.execute(select(self.model).where(self.model.email == email))
        return result.scalar_one_or_none()
