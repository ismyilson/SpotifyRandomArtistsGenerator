import os

from contextlib import contextmanager

from sqlmodel import Session, create_engine

_engine = create_engine(os.environ.get('SPOTIFY_RANDOM_GEN_DATABASE_ID'))


@contextmanager
def get_session():
    with Session(_engine) as session:
        yield session
