from functools import lru_cache
from typing import Literal

from pydantic import PostgresDsn, SecretStr, computed_field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "Project Management Platform"
    APP_VERSION: str = "0.0.1"
    APP_ENV: Literal["development", "test", "production"] = "development"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+psycopg",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD.get_secret_value(),
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DB,
            )
        )

    @field_validator("API_V1_PREFIX")
    @classmethod
    def validate_prefix(cls, v: str) -> str:
        if not v.startswith("/") or v.endswith("/"):
            raise ValueError("API_V1_PREFIX must start with '/' and not end with '/'")
        return v

    @model_validator(mode="after")
    def no_debug_in_production(self) -> "Settings":
        if self.APP_ENV == "production" and self.DEBUG:
            raise ValueError("DEBUG must be False in production")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
