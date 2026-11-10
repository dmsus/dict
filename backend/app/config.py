import os
from functools import lru_cache
from urllib.parse import quote_plus

from pydantic import BaseModel


class Settings(BaseModel):
    """Настройки приложения. Все значения берутся только из переменных окружения."""

    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    @property
    def database_url(self) -> str:
        # Async-движок SQLAlchemy через psycopg (psycopg3).
        return (
            "postgresql+psycopg://"
            f"{quote_plus(self.db_user)}:{quote_plus(self.db_password)}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings(
        db_host=os.environ["DB_HOST"],
        db_port=int(os.getenv("DB_PORT", "5432")),
        db_name=os.environ["DB_NAME"],
        db_user=os.environ["DB_USER"],
        db_password=os.environ["DB_PASSWORD"],
    )
