from datetime import datetime

from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, DateTime, func


class ProcessingSong(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(sa_column=Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    ))
    song_fullname: str = Field(unique=True, index=True)
