import uuid

from sqlalchemy import Column, UUID, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

from utils.abstractions.models import AbstractBaseModel


class File(AbstractBaseModel):
    __tablename__ = 'file'
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    url = Column(String(255))
    s3_url = Column(String(255))
    current_bytes = Column(Integer, default=0, nullable=True)
    is_stream = Column(Boolean, nullable=True)
    is_ready = Column(Boolean, default=True)
    file_metadata = relationship("FileMetaData", uselist=False, backref=backref("file", uselist=False))


class FileMetaData(AbstractBaseModel):
    __tablename__ = 'file_meta'
    id = Column(Integer, primary_key=True)
    original_title = Column(String(255))
    size = Column(Integer)
    content_type = Column(String(255))
    extension = Column(String(255))
    file_id = Column(UUID, ForeignKey('file.id'))
