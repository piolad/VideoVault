from sqlalchemy import Integer, String, ForeignKey, Text, DateTime
from sqlalchemy import Enum as SqlAlchEnum
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, Field,ConfigDict
from typing import Optional
from enum import Enum
from datetime import datetime

from .db import db

class AccountStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELETED = "deleted"
    SUSPENED = "suspended"

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # displayed name
    name: Mapped[str] = mapped_column(String(45), nullable=False)
    
    bio: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped["datetime"] = mapped_column(DateTime(timezone=True),nullable=False)

    deleted_at: Mapped[Optional["datetime"]] = mapped_column(DateTime(timezone=True),nullable=True)

    status: Mapped[AccountStatus] = mapped_column( SqlAlchEnum(AccountStatus, name="account_status", native_enum=True, validateStrings=True), default=AccountStatus.INACTIVE )



# for pydantic
class UserCreate(BaseModel):
    # to prevent some injections
    model_config = ConfigDict(extra="forbid")

    id: Optional[int] = None
    name: str = Field(min_length=1, max_length=255)
    
    bio: str = Field(default="", max_length=50_000)

    status: AccountStatus = AccountStatus.INACTIVE
