from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    __abstract__ = True

    @classmethod
    @declared_attr
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"

    id = Column(Integer, primary_key=True, index=True)


class TimeStampMixin:
    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True), default=func.now())

    @declared_attr
    def updated_at(cls):
        return Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())


class CreatedAtMixin:
    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True), default=func.now())


class UpdatedAtMixin:
    @declared_attr
    def updated_at(cls):
        return Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
