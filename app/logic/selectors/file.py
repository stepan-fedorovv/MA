import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db import models


async def find_by_id(*, db: AsyncSession, id: uuid.UUID):
    result = await db.execute(
        select(models.File).filter_by(id=id).options(selectinload(models.File.file_metadata))
    )
    return result.scalar()
