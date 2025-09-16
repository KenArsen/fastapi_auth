from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum as SQLEnum
from src.models.base import Base, TimeStampMixin
from src.models.enam import Role


class Account(Base, TimeStampMixin):
    role: Mapped[Role] = mapped_column(SQLEnum(Role), server_default=Role.USER)
    username: Mapped[str] = mapped_column(String(100), nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    def __str__(self) -> str:
        return f"<Account(id={self.id}, role={self.role} username={self.username}, email={self.email})>"

    def __repr__(self) -> str:
        return str(self)
