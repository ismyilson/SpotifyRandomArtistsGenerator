import time
import logging

from datetime import datetime, timezone

from logging.handlers import RotatingFileHandler
from pathlib import Path

from config import PLAYLIST_ID
from services import (
    artist_services
)

import spotipy
from spotipy.oauth2 import SpotifyOAuth

MAX_TRIES = 5

handler = RotatingFileHandler(
    Path(__file__).parent / 'spotify_playlist_maker.log', 
    maxBytes=2 * 1024 * 1024, 
    backupCount=5
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        handler,
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def run():
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=['playlist-modify-public'], open_browser=False))

    playlist_data = spotify.playlist_items(PLAYLIST_ID)
    track_list = [item['track']['id'] for item in playlist_data['items']]

    if track_list:
        spotify.playlist_remove_all_occurrences_of_items(PLAYLIST_ID, track_list)

    artists = artist_services.get_artists_used_for_playlist(False, limit = 15)
    if not artists:
        logger.info(f'No results')
        return False
    
    top_tracks_ids = []
    for artist in artists:
        logger.info(f'Got artist: "{artist.name}", grabbing top songs')

        tracks = spotify.artist_top_tracks(artist.spotify_id)['tracks']
        if len(tracks) == 0:
            try:
                album = spotify.artist_albums(artist.spotify_id)['items'][0]
                tracks = spotify.album_tracks(album['id'])['items']
            except IndexError as e:
                logger.info(f'Broken artist "{artist.name}", no songs? Deleting artist')
                artist_services.delete_artist(artist.id)
                return False

        idx = 0
        while tracks[idx]['id'] in top_tracks_ids:
            idx += 1

        logger.info(f'Using track: "{tracks[idx]['id']}"')
        top_tracks_ids.append(tracks[idx]['id'])
    
    spotify.playlist_add_items(PLAYLIST_ID, top_tracks_ids)

    now = datetime.now(timezone.utc)
    for artist in artists:
        artist.used_for_playlist = True
        artist.used_for_playlist_datetime = now
    
    artist_services.update_artists(artists)
    
    return True


if __name__ == '__main__':
    time_start = time.time()

    tries = 0
    while not run():
        tries += 1

        if tries >= MAX_TRIES:
            logger.info(f'Run failed more than {MAX_TRIES} times, aborting')
            exit(1)

        logger.info(f'Run failed, retrying..')

    logger.info(f'Run finished in {time.time() - time_start} seconds')
