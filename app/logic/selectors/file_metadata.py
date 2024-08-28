from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import models


async def find_by_file_id(
        file_id: int,
        db: AsyncSession,
):
    result = await db.execute(
        select(models.FileMetaData).filter_by(file_id=file_id)
    )
    return result.first()
