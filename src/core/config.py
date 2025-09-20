from typing import List, Optional, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # Database
    DB_ENGINE: str = "sqlite"  # postgres | sqlite
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "app"
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"

    # CORS
    CORS_ORIGINS: Union[List[str], str] = ["*"]

    # Cookies / JWT
    COOKIE_SECURE: bool = False
    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: Optional[str] = None
    JWT_ACCESS_COOKIE_NAME: str = "access_token"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @classmethod
    @field_validator("JWT_SECRET_KEY")
    def validate_secret(cls, v):
        if not v:
            raise ValueError("JWT_SECRET_KEY обязательно нужно указать")
        return v

    @classmethod
    @field_validator("CORS_ORIGINS", mode="before")
    def parse_cors(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    @property
    def database_url(self) -> str:
        if self.DB_ENGINE == "sqlite":
            return "sqlite+aiosqlite:///./sqlite.db"
        elif self.DB_ENGINE == "postgres":
            return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        else:
            raise ValueError(f"Неподдерживаемый DB_ENGINE: {self.DB_ENGINE}")


settings = Settings()
