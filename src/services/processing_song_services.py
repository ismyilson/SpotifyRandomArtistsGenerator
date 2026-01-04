from models.processing_song import ProcessingSong
from sqlmodel import select, delete
from sqlalchemy.dialects.postgresql import insert
from database import get_session


def add_processing_song(song_name):
    processing_song = ProcessingSong(
        song_fullname=song_name
    )

    with get_session() as session:
        session.add(processing_song)
        session.commit()
        session.refresh(processing_song)

    return processing_song


def bulk_add_processing_songs(processing_songs):
    data = [song.model_dump(exclude=['id']) for song in processing_songs]
    with get_session() as session:
        stmt = insert(ProcessingSong).values(data)
        stmt = stmt.on_conflict_do_nothing(index_elements=['song_fullname'])
        session.exec(stmt)
        session.commit()


def get_by_id(id):
    with get_session() as session:
        processing_song = session.get(ProcessingSong, id)
    
    return processing_song


def get_processing_songs(limit = 10):
    with get_session() as session:
        stmt = select(ProcessingSong).limit(limit)
        processing_songs = session.exec(stmt).all()
    
    return processing_songs


def delete_processing_song(id):
    processing_song = get_by_id(id)
    if not processing_song:
        return

    with get_session() as session:
        session.delete(processing_song)
        session.commit()


def delete_processing_songs(ids):
    with get_session() as session:
        stmt = delete(ProcessingSong).where(ProcessingSong.id.in_(ids))
        session.exec(stmt)
        session.commit()
