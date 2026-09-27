from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BIOVERITY_", env_file=".env")

    database_url: str = Field(
        default="postgresql+psycopg://bioverity:bioverity@localhost:5433/bioverity"
    )


settings = Settings()
