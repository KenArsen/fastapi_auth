from typing import Any, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.accounts.models import Account


class AccountRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, pk: int) -> Account | None:
        result = await self.session.execute(select(Account).where(Account.id == pk))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Account | None:
        result = await self.session.execute(select(Account).where(Account.email == email))
        return result.scalar_one_or_none()

    async def create(self, account: Account) -> Account:
        self.session.add(account)
        await self.session.commit()
        await self.session.refresh(account)
        return account

    async def update(self, pk: int, data: dict[str, Any]) -> Account | None:
        account = await self.get_by_id(pk)
        if not account:
            return None
        for key, value in data.items():
            setattr(account, key, value)
        await self.session.commit()
        await self.session.refresh(account)
        return account

    async def delete(self, pk: int) -> bool:
        account = await self.get_by_id(pk)
        if account:
            await self.session.delete(account)
            await self.session.commit()
            return True
        return False

    async def all(self) -> Sequence[Account]:
        result = await self.session.execute(select(Account))
        return result.scalars().all()