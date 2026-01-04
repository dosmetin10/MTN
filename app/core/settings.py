from functools import lru_cache
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    url: str = "sqlite:///./mtn.sqlite"
    echo: bool = False


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")

    app_name: str = "MTN Enerji Backend"
    environment: str = "local"
    database: DatabaseSettings = DatabaseSettings()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
