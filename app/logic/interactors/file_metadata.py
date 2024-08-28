import uuid

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas import file as file_schemas
from app.db import models
from utils import model as model_actions


async def create_file_metadata(
        *,
        db: AsyncSession,
        file: UploadFile,
        file_id: uuid.UUID,
        original_filename: str
):
    metadata = file_schemas.FileMetaDataDto(
        original_title=original_filename,
        size=file.size,
        content_type=file.content_type,
        extension=original_filename.split('.')[-1],
        file_id=file_id
    )
    await model_actions.create_model_instance(
        instance=models.FileMetaData,
        db=db,
        validated_data=metadata.model_dump()
    )
