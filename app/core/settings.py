from functools import lru_cache
from pathlib import Path, WindowsPath
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

config = Config(".env")


class APPSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
    )
    VERSION: str = config("VERSION", cast=str, default="1.0.0")
    BASE_DIR: WindowsPath = Path(__file__).resolve().parent.parent
    MEDIA_ROOT: WindowsPath = BASE_DIR / "media/"
    DEBUG: bool = config("DEBUG", cast=bool, default=False)
    ENV: str = config("ENV", cast=str, default="TEST")

    AWS_ACCESS_KEY_ID: str = config('AWS_ACCESS_KEY_ID', default='your_access_key')
    AWS_SECRET_ACCESS_KEY: str = config('AWS_SECRET_ACCESS_KEY', default='your_secret_key')
    AWS_REGION_NAME: str = config('AWS_REGION_NAME', default='your_region')

    POSTGRES_SERVER: str = config("POSTGRES_SERVER", cast=str, default="localhost")
    POSTGRES_PORT: int = config("POSTGRES_PORT", cast=int, default=5432)
    POSTGRES_USER: str = config("POSTGRES_USER", cast=str, default="ma_test")
    POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", cast=str, default="ma_test")
    POSTGRES_DB: str = config("POSTGRES_DB", cast=str, default="ma_test")

    SQL_DEBUG: bool = config("SQL_DEBUG", cast=bool, default=False)

    API_ROUTE: str = config("API_ROUTE", cast=str, default="/api")
    API_ROOT_PATH: str = config("API_ROOT_PATH", default="")
    LOGGING_LEVEL: str = config("LOGGING_LEVEL", cast=str, default="INFO")
    LOGGING_SERIALIZE: bool = config("LOGGING_SERIALIZE", cast=bool, default=False)

    HTTP_CLIENT_MAX_ATTEMPTS: int = config(
        "HTTP_CLIENT_MAX_ATTEMPTS", cast=int, default=3
    )
    HTTP_CLIENT_START_TIMEOUT: float = config(
        "HTTP_CLIENT_START_TIMEOUT", cast=float, default=0.1
    )
    HTTP_CLIENT_MAX_TIMEOUT: float = config(
        "HTTP_CLIENT_MAX_TIMEOUT", cast=float, default=30.0
    )
    HTTP_CLIENT_BACKOFF_FACTOR: float = config(
        "HTTP_CLIENT_BACKOFF_FACTOR", cast=float, default=2.0
    )
    HTTP_CLIENT_DNS_MAX_ATTEMPTS: int = config(
        "HTTP_CLIENT_DNS_MAX_ATTEMPTS", cast=int, default=4
    )
    HTTP_CLIENT_DNS_TIMEOUT: float = config(
        "HTTP_CLIENT_DNS_TIMEOUT", cast=float, default=5.0
    )
    HTTP_CLIENT_RAISE_FOR_STATUS: bool = config(
        "HTTP_CLIENT_RAISE_FOR_STATUS", cast=bool, default=False
    )
    HTTP_CLIENT_RETRY_STATUSES: Optional[CommaSeparatedStrings] = config(
        "HTTP_CLIENT_RETRY_STATUSES", cast=CommaSeparatedStrings, default=None
    )
    MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=1)
    MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)


@lru_cache()
def get_app_settings() -> APPSettings:
    return APPSettings()
