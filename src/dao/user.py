from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import Account

class AccountCRUD:
    @staticmethod
    async def get_by_email(session: AsyncSession, email: str) -> Account | None:
        result = await session.execute(select(Account).where(Account.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(session: AsyncSession, account: Account) -> Account:
        account.set_password(account.password)
        session.add(account)
        await session.commit()
        await session.refresh(account)
        return account