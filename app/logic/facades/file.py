from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import models
from app.logic.interactors import file as file_interactors
from app.logic.interactors.file import upload_file_by_stream
from app.logic.selectors.file import find_by_id


async def upload(
        *,
        db: AsyncSession,
        file: UploadFile,
        stream: bool = False,
        file_id: str
):
    if stream and not file_id:
        raise HTTPException(
            detail='Нельзя использовать стриминговую загрузку без file_id',
            status_code=418
        )
    if stream:
        instance = await upload_file_by_stream(db=db, file=file, file_id=file_id)
        return instance
    instance = await file_interactors.upload_file(
        db=db,
        file=file
    )
    return instance


async def find_file_by_id(
        *,
        db: AsyncSession,
        file_id: str
) -> models.File:
    result = await find_by_id(
        db=db,
        id=file_id,
    )
    if not result:
        raise HTTPException(detail='File not found', status_code=404)
    return result
