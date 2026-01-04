from models.artist import Artist
from sqlmodel import select, func
from database import get_session


def add_artist(spotify_id, name, origin_song, origin_song_id):
    artist = Artist(
        spotify_id=spotify_id,
        name=name,
        origin_song=origin_song,
        origin_song_id=origin_song_id
    )

    with get_session() as session:
        session.add(artist)
        session.commit()
        session.refresh(artist)
    
    return artist


def update_artist(artist):
    with get_session() as session:
        session.add(artist)
        session.commit()
        session.refresh(artist)
    
    return artist


def update_artists(artists):
    with get_session() as session:
        session.add_all(artists)
        session.commit()
    
    return artists


def bulk_add_artists(artists):
    with get_session() as session:
        session.add_all(artists)
        session.commit()


def get_by_id(id):
    with get_session() as session:
        artist = session.get(Artist, id)
    
    return artist


def get_by_spotify_id(spotify_id):
    with get_session() as session:
        stmt = select(Artist).where(Artist.spotify_id == spotify_id)
        artist = session.exec(stmt).first()
    
    return artist


def get_artists(limit = 10):
    with get_session() as session:
        stmt = select(Artist).limit(limit)
        artists = session.exec(stmt).all()
    
    return artists


def get_artists_used_for_playlist(used, limit = 15):
    with get_session() as session:
        stmt = select(Artist).where(Artist.used_for_playlist == used).order_by(func.random()).limit(limit)
        artists = session.exec(stmt).all()
    
    return artists


def get_artists_used_for_recommended(used, limit = 10):
    with get_session() as session:
        stmt = select(Artist).where(Artist.used_for_recommended == used).limit(limit)
        artists = session.exec(stmt).all()
    
    return artists


def artist_exists(spotify_id):
    artist = get_by_spotify_id(spotify_id)
    return not (artist is None)


def delete_artist(id):
    artist = get_by_id(id)
    if not artist:
        return

    with get_session() as session:
        session.delete(artist)
        session.commit()
