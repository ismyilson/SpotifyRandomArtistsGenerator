import time

from services import (
    artist_services,
    processing_song_services,
    reccobeats_services
)

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

MAX_REQUESTS = 10


def recommendation_finder():
    artists = artist_services.get_artists_used_for_recommended(False)
    if not artists:
        print(f'No artists found to use for recommended')
        return
    
    print(f'Processing {len(artists)} artists not used for recommended')

    reqs = 0
    for artist in artists:
        recommended_songs = reccobeats_services.get_recommended([artist.origin_song_id])
        reqs += 1
        if not recommended_songs:
            continue

        recommended_songs = recommended_songs['content']
        print(f'Found {len(recommended_songs)} songs for artist "{artist.name}"')
        for song in recommended_songs:
            spotify_song_id = song['href']
            song_name = song['trackTitle']
            if not spotify_song_id:
                continue

            spotify_song_id = spotify_song_id[spotify_song_id.rindex('/')+1:]

            song_artists = song['artists']
            for song_artist in song_artists:
                spotify_artist_id = song_artist['href']
                spotify_artist_id = spotify_artist_id[spotify_artist_id.rindex('/')+1:]
                if not spotify_artist_id:
                    continue

                if artist_services.artist_exists(spotify_artist_id):
                    print(f'Skipping artist "{song_artist["name"]}", Spotify ID already in database')
                    continue
                
                artist_services.add_artist(
                    spotify_artist_id,
                    song_artist['name'],
                    song_name,
                    spotify_song_id
                )
                print(f'Added "{song_artist["name"]}" to database')
        
        artist.used_for_recommended = True
        
        if reqs >= MAX_REQUESTS:
            print(f'Waiting 1.5 seconds for Reccobeats requests rate-limit')
            time.sleep(1.5)
            reqs = 0
    
    artist_services.update_artists(artists)


def process():
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
    processing_songs = processing_song_services.get_processing_songs(50)

    if not processing_songs:
        print('No songs to process')
        return 0

    reqs = 0
    for song in processing_songs:
        print(f'Processing "{song.song_fullname}"')

        result = spotify.search(song.song_fullname)['tracks']['items']
        reqs += 1

        if len(result) == 0:
            print(f'Skipping "{song.song_fullname}", cant find on Spotify')
            continue

        result = result[0]
        song_id = result['id']
        song_artists = result['artists']
        for artist_data in song_artists:
            spotify_id = artist_data['id']
            artist_name = artist_data['name']

            if artist_services.artist_exists(spotify_id):
                print(f'Skipping artist "{artist_name}", Spotify ID already in database')
                continue

            print(f'Adding artist "{artist_name}" to database')
            artist_services.add_artist(spotify_id, artist_name, song.song_fullname, song_id)
        
        if reqs >= MAX_REQUESTS:
            print(f'Waiting 1.5 seconds for Spotify requests rate-limit')
            time.sleep(1.5)
            reqs = 0
    
    ids = [song.id for song in processing_songs]
    processing_song_services.delete_processing_songs(
        ids
    )
    
    return len(ids)


def run():
    time_start = time.time()

    process()

    recommendation_finder()

    print(f'Run finished in {time.time() - time_start} seconds')


if __name__ == '__main__':
    run()
