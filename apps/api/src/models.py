from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, Field,ConfigDict
from typing import Optional

from .db import db

class Video(db.Model):
    __tablename__ = "videos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str]

class VideoCreate(BaseModel):
    name: str = Field(min_length=1)
    id: Optional[int] = None

class VideoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str