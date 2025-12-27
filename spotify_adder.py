import time

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from cloudflare_services import cloudflare_manager

MAX_REQUESTS = 10


def run():
    time_start = time.time()

    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
    processing_list = cloudflare_manager.get_processing(limit = 50)

    songs_to_remove = []
    reqs = 0
    for row in processing_list:
        song_fullname = row['song_fullname']
        print(f'Processing "{song_fullname}"')

        result = spotify.search(song_fullname)['tracks']['items']
        reqs += 1

        songs_to_remove.append(song_fullname)
        if len(result) == 0:
            print(f'Skipping "{song_fullname}", cant find on Spotify')
            continue

        result = result[0]
        song_id = result['id']
        song_artists = result['artists']
        for artist_data in song_artists:
            spotify_id = artist_data['id']
            artist_name = artist_data['name']

            if cloudflare_manager.artist_exists(spotify_id):
                print(f'Skipping artist "{artist_name}", Spotify ID already in database')
                continue

            print(f'Adding artist "{artist_name}" to database')
            cloudflare_manager.add_artist(spotify_id, artist_name, song_fullname, song_id)
        
        if reqs >= MAX_REQUESTS:
            print(f'Waiting 1.5 seconds for Spotify requests rate-limit')
            time.sleep(1.5)
            reqs = 0
    
    if len(songs_to_remove) > 0:
        cloudflare_manager.delete_from_processing(songs_to_remove)
    
    print(f'Run finished in {time.time() - time_start} seconds')


if __name__ == '__main__':
    run()
