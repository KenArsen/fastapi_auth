from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from passlib.context import CryptContext
from src.models.base import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Account(Base):
    username: Mapped[str] = mapped_column(String(100), nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    def __str__(self) -> str:
        return f"<Account(id={self.id}, username={self.username}, email={self.email})>"

    def __repr__(self) -> str:
        return str(self)

    def set_password(self, password: str) -> None:
        self.password = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password)
