from sqlalchemy import Integer, String, ForeignKey, Text, DateTime
from sqlalchemy import Enum as SqlAlchEnum
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, Field,ConfigDict
from typing import Optional
from enum import Enum

from .db import db

class VideoVisibility(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    UNLISTED = "unlisted"

class VideoStatus(str, Enum):
    UPLOADING = "uploading"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"
    DELETED = "deleted"

class Video(db.Model):
    __tablename__ = "videos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False) # todo: add fuzzy index for searching

    description: Mapped[str] = mapped_column(Text, nullable=False)

    visibility: Mapped[VideoVisibility]  = mapped_column( SqlAlchEnum(VideoVisibility, name="video_visibility", native_enum=True, validateStrings=True) )

    status: Mapped[VideoStatus]  = mapped_column( SqlAlchEnum(VideoStatus, name="video_status", native_enum=True, validateStrings=True) )

    blob_key: Mapped[str] = mapped_column(String(1024, nullable=False))

    hls_master_key: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)

    duration_seconds: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped["datetime"] = mapped_column(DateTime(timezone=True),nullable=False)
    
    uploaded_at: Mapped[Optional["datetime"]] = mapped_column(DateTime(timezone=True),nullable=True)
    deleted_at: Mapped[Optional["datetime"]] = mapped_column(DateTime(timezone=True),nullable=True)
    
    #version: Mapped[int] # todo, for concurrency
    # like_count: Mapped[int] # caching, todo



# for pydantic
class VideoCreate(BaseModel):
    # to prevent injections
    model_config = ConfigDict(extra="forbid") 
    name: str = Field(min_length=1)
    id: Optional[int] = None

class VideoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str