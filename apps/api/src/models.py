from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .db import db

class Video(db.Model):
    __tablename__ = "videos"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
