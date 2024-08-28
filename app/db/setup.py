import logging

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.core import config

logger = logging.getLogger(__name__)
Base = declarative_base()

SQLALCHEMY_DATABASE_URL = (f"postgresql+asyncpg://"
                           f"{config.POSTGRES_USER}:"
                           f"{config.POSTGRES_PASSWORD}@"
                           f"{config.POSTGRES_DB}:{config.POSTGRES_PORT}/ma_test")
async_engine = create_async_engine(
    url=SQLALCHEMY_DATABASE_URL,
)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    future=True,
)
