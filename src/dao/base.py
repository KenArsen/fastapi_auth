from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import Type, TypeVar

T = TypeVar("T")


class BaseDAO:
    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, obj_id: int) -> T | None:
        result = await self.session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalar_one_or_none()

    async def create(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, obj_id: int, values: dict) -> T | None:
        await self.session.execute(
            update(self.model).where(self.model.id == obj_id).values(**values)
        )
        await self.session.commit()
        return await self.get_by_id(obj_id)

    async def delete(self, obj_id: int) -> None:
        await self.session.execute(delete(self.model).where(self.model.id == obj_id))
        await self.session.commit()
