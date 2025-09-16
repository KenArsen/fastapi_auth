from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    CORS_ORIGINS: List[str] = ["*"]
    COOKIE_SECURE: bool = False
    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str
    JWT_ACCESS_COOKIE_NAME: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @property
    def database_url(self) -> str:
        return "sqlite+aiosqlite:///./sqlite.db"


settings = Settings()
