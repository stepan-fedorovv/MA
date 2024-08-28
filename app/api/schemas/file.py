import uuid

from utils.abstractions.serializers import BaseSchema


class FileMetaDataDto(BaseSchema):
    file_id: uuid.UUID
    original_title: str
    size: int
    content_type: str
    extension: str


class FileDto(BaseSchema):
    id: uuid.UUID
    current_bytes: int
    is_ready: bool | None
    is_stream: bool | None
    s3_url: str
    url: str
    file_metadata: FileMetaDataDto
