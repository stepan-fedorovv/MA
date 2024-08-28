import typing
import uuid

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload, lazyload

from app.api.dependencies.session import get_db
from app.api.schemas.file import FileDto
from app.db import models
from app.logic.facades import file as file_facades
from app.logic.facades.file import find_file_by_id
from app.logic.selectors.file import find_by_id

router = APIRouter()


@router.post(
    "/upload/",
    description='Uploading files to server and cloud',
    response_model=FileDto
)
async def upload(
        file: UploadFile = File(...),
        stream: typing.Annotated[bool, Form()] = None,
        file_id: typing.Annotated[str, Form()] = None,
        db: AsyncSession = Depends(get_db)
):
    file_instance = await file_facades.upload(
        db=db,
        file=file,
        stream=stream,
        file_id=file_id,
    )
    return file_instance


@router.get('/{file_id}/', response_model=FileDto, description='Find file by id', )
async def get_file(
        file_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),

):
    file_instance = await find_file_by_id(
        db=db,
        file_id=file_id,
    )
    return file_instance
