import time
import logging

from logging.handlers import RotatingFileHandler
from pathlib import Path
from services import (
    kworb_services,
    processing_song_services,
)
from models.processing_song import ProcessingSong

handler = RotatingFileHandler(
    Path(__file__).parent / 'artist_discoverer.log', 
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


def run_song_finder():
    songs_names = kworb_services.get_kworb_songs()
    logger.info(f'Found {len(songs_names)} songs')

    songs = [
        ProcessingSong(
            song_fullname=song
        ) for song in songs_names
    ]
    processing_song_services.bulk_add_processing_songs(songs)


def run():
    time_start = time.time()

    run_song_finder()

    logger.info(f'Run finished in {time.time() - time_start} seconds')


if __name__ == '__main__':
    run()
