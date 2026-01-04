import os
from config import ARTIST_DATABASE_ID
from contextlib import contextmanager
from sqlmodel import Session, create_engine

_engine = create_engine(ARTIST_DATABASE_ID)


@contextmanager
def get_session():
    with Session(_engine) as session:
        yield session
