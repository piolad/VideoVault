from sqlalchemy import Integer, String, ForeignKey, Text, DateTime
from sqlalchemy import Enum as SqlAlchEnum
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, Field,ConfigDict
from typing import Optional
from enum import Enum
from datetime import datetime

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

    title: Mapped[str] = mapped_column(String(255), nullable=False) # TODO: add fuzzy index for searching

    description: Mapped[str] = mapped_column(Text, nullable=False)

    visibility: Mapped[VideoVisibility]  = mapped_column( SqlAlchEnum(VideoVisibility, name="video_visibility", native_enum=True, validateStrings=True) )

    status: Mapped[VideoStatus]  = mapped_column( SqlAlchEnum(VideoStatus, name="video_status", native_enum=True, validateStrings=True), default=VideoStatus.UPLOADING )

    blob_key: Mapped[str] = mapped_column(String(1024), nullable=False)

    hls_master_key: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)

    duration_seconds: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped["datetime"] = mapped_column(DateTime(timezone=True),nullable=False)
    
    uploaded_at: Mapped[Optional["datetime"]] = mapped_column(DateTime(timezone=True),nullable=True)
    deleted_at: Mapped[Optional["datetime"]] = mapped_column(DateTime(timezone=True),nullable=True)
    
    # version: Mapped[int] # TODO, for concurrency
    # like_count: Mapped[int] # caching, TODO,



# for pydantic
class VideoCreate(BaseModel):
    # to prevent some injections
    model_config = ConfigDict(extra="forbid")

    id: Optional[int] = None
    title: str = Field(min_length=1, max_length=255)
    
    description: str = Field(default="", max_length=50_000)

    visibility: VideoVisibility = VideoVisibility.PRIVATE

class VideoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    title: str
    description: str
    visibility: VideoVisibility
    status: VideoStatus
    
    blob_key: str
    hls_master_key: Optional[str]
    
    duration_seconds: int

    created_at: datetime
    uploaded_at: Optional[datetime]
    deleted_at: Optional[datetime]


# TODO: VideoUpdate