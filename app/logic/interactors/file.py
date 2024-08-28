import os
import uuid

import aioboto3
import aiofiles
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import UploadFile
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import config
from app.db import models
from app.logic.interactors import file_metadata
from app.logic.selectors.file import find_by_id
from app.logic.selectors.file_metadata import find_by_file_id
from utils import model as model_actions

MAX_CHUNK_SIZE: int = 1024 * 1024


async def upload_to_cloud(*, file: UploadFile, filename: str) -> dict[str, str] | None:
    session = aioboto3.Session(
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        region_name=config.AWS_REGION_NAME
    )
    try:
        async with session.client('s3') as s3_client:
            file_content = await file.read()

            await s3_client.put_object(
                Bucket='some_bucket_name',
                Key=filename,
                Body=file_content
            )

        return {"message": "File uploaded successfully"}

    except (BotoCoreError, ClientError):
        """
        Стоит заглушка, здесь должна выбрасываться ошибка.
        """
        pass


async def _file_params(
        *,
        file: UploadFile,
        file_id: uuid.UUID | None = None
) -> tuple[str, str, str]:
    original_filename = file.filename
    new_filename = str(uuid.uuid4()) if file_id is None else file_id
    file_path = os.path.join(
        config.MEDIA_ROOT,
        f"{new_filename}.{original_filename.split('.')[-1]}"
    )
    return original_filename, file_path, new_filename


async def _save_file_locally(
        *,
        file: UploadFile,
        file_path: str,
) -> None:
    async with aiofiles.open(file_path, "wb") as output:
        while chunk := await file.read():
            await output.write(chunk)


async def _save_file_locally_by_stream(
        *,
        db: AsyncSession,
        current_bytes: int,
        file_path: str,
        file_instance: models.File,
        file: UploadFile
) -> None:
    current_bytes = current_bytes or 0
    async with aiofiles.open(file_path, "wb") as output:
        if current_bytes == file.size:
            await db.execute(
                update(file_instance).values(
                    is_ready=True
                )
            )
            await db.commit()
            return
        while chunk := await file.read(MAX_CHUNK_SIZE):
            await output.write(chunk)
        await db.execute(
            update(models.File).values(current_bytes=current_bytes + MAX_CHUNK_SIZE)
        )
        await db.commit()


async def upload_file(
        *,
        db: AsyncSession,
        file: UploadFile
) -> models.File:
    original_filename, file_path, new_filename = await _file_params(file=file)
    await _save_file_locally(
        file=file,
        file_path=file_path
    )
    await model_actions.create_model_instance(
        instance=models.File,
        db=db,
        validated_data={
            'id': new_filename,
            'url': file_path,
            's3_url': 'some_s3_url'
        }
    )
    await file_metadata.create_file_metadata(
        db=db,
        file=file,
        file_id=new_filename,
        original_filename=original_filename
    )
    await upload_to_cloud(file=file, filename=new_filename)
    file_instance = await find_by_id(
        db=db,
        id=new_filename
    )
    return file_instance


async def upload_file_by_stream(*, db: AsyncSession, file: UploadFile, file_id: str) -> models.File:
    original_filename, file_path, new_filename = await _file_params(
        file=file,
        file_id=file_id
    )
    file_instance, _ = await model_actions.get_or_create(
        db=db,
        model=models.File,
        validated_data={
            'id': new_filename,
            'url': file_path,
            's3_url': 'some_s3_url',
            'is_stream': True,
            'is_ready': False
        }
    )
    if file_instance.is_ready:
        return file_instance

    await _save_file_locally_by_stream(
        db=db,
        current_bytes=file_instance.current_bytes,
        file_instance=file_instance,
        file=file,
        file_path=file_path
    )
    metadata = await find_by_file_id(
        db=db,
        file_id=file_id
    )
    if not metadata:
        await file_metadata.create_file_metadata(
            db=db,
            file=file,
            file_id=file_id,
            original_filename=original_filename
        )
    await db.commit()
    await upload_to_cloud(file=file, filename=new_filename)
    file_instance = await find_by_id(
        db=db,
        id=new_filename
    )
    return file_instance
