from datetime import datetime

from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, DateTime, func


class Artist(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(sa_column=Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    ))
    spotify_id: str = Field(max_length=100, unique=True, index=True, nullable=False)
    name: str = Field(max_length=255, index=True)
    origin_song: Optional[str] = Field(default=None)
    origin_song_id: Optional[str] = Field(max_length=100, default=None)
    used_for_recommended: bool = Field(default=False, index=True)
    used_for_playlist: bool = Field(default=False, index=True)
