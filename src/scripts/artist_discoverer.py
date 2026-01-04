import time

from services import (
    kworb_services,
    processing_song_services,
)
from models.processing_song import ProcessingSong

MAX_REQUESTS = 10


def run_song_finder():
    songs_names = kworb_services.get_kworb_songs()
    print(f'Processing {len(songs_names)} songs')

    songs = [
        ProcessingSong(
            song_fullname=song
        ) for song in songs_names
    ]
    processing_song_services.bulk_add_processing_songs(songs)


def run():
    time_start = time.time()

    run_song_finder()

    print(f'Run finished in {time.time() - time_start} seconds')


if __name__ == '__main__':
    run()
