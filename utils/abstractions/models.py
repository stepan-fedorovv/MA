import typing

from sqlalchemy import Column, UUID

from app.db.setup import Base

SQLAlchemyModel = typing.TypeVar("SQLAlchemyModel", bound=Base)


class AbstractBaseModel(Base):
    """
    Abstract base model for whole models in service
    """
    __abstract__ = True
