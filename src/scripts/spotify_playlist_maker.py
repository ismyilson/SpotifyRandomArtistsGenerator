import time

from services import (
    artist_services
)

import spotipy
from spotipy.oauth2 import SpotifyOAuth

PLAYLIST_ID = '1wVT9oPaOYQfLxMMdC2EJg'

MAX_TRIES = 5


def run():
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=['playlist-modify-public']))

    playlist_data = spotify.playlist_items(PLAYLIST_ID)
    track_list = [item['track']['id'] for item in playlist_data['items']]

    if track_list:
        spotify.playlist_remove_all_occurrences_of_items(PLAYLIST_ID, track_list)

    artists = artist_services.get_artists_used_for_playlist(False, limit = 15)
    if not artists:
        print(f'No results')
        return False
    
    top_tracks_ids = []
    for artist in artists:
        print(f'Got artist: "{artist.name}", grabbing top songs')

        tracks = spotify.artist_top_tracks(artist.spotify_id)['tracks']
        if len(tracks) == 0:
            try:
                album = spotify.artist_albums(artist.spotify_id)['items'][0]
                tracks = spotify.album_tracks(album['id'])['items']
            except IndexError as e:
                print(f'Broken artist "{artist.name}", no songs? Deleting artist')
                artist_services.delete_artist(artist.id)
                return False

        idx = 0
        while tracks[idx]['id'] in top_tracks_ids:
            idx += 1

        print(f'Using track: "{tracks[idx]['id']}"')
        top_tracks_ids.append(tracks[idx]['id'])
    
    spotify.playlist_add_items(PLAYLIST_ID, top_tracks_ids)

    for artist in artists:
        artist.used_for_playlist = True
    artist_services.update_artists(artists)
    
    return True


if __name__ == '__main__':
    time_start = time.time()

    tries = 0
    while not run():
        tries += 1

        if tries >= MAX_TRIES:
            print(f'Run failed more than {MAX_TRIES} times, aborting')
            exit(1)

        print(f'Run failed, retrying..')

    print(f'Run finished in {time.time() - time_start} seconds')
