import time

from services import (
    artist_services
)

import spotipy
from spotipy.oauth2 import SpotifyOAuth

PLAYLIST_ID = '1wVT9oPaOYQfLxMMdC2EJg'


def run():
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=['playlist-modify-public']))

    playlist_data = spotify.playlist_items(PLAYLIST_ID)
    track_list = [item['track']['id'] for item in playlist_data['items']]

    if track_list:
        spotify.playlist_remove_all_occurrences_of_items(PLAYLIST_ID, track_list)

    artists = artist_services.get_artists_used_for_playlist(False, limit = 15)
    if not artists:
        print(f'No results')
        return
    
    top_tracks_ids = []
    for artist in artists:
        print(f'Got artist: "{artist.name}", grabbing top songs')

        tracks = spotify.artist_top_tracks(artist.spotify_id)['tracks']
        if len(tracks) == 0:
            album = spotify.artist_albums(artist.spotify_id)['items'][0]
            tracks = spotify.album_tracks(album['id'])['items']

        idx = 0
        while tracks[idx]['id'] in top_tracks_ids:
            idx += 1

        print(f'Using track: "{tracks[idx]['id']}"')
        top_tracks_ids.append(tracks[idx]['id'])

        artist.used_for_playlist = True
    
    spotify.playlist_add_items(PLAYLIST_ID, top_tracks_ids)
    artist_services.update_artists(artists)
    print('Done')


if __name__ == '__main__':
    time_start = time.time()

    run()

    print(f'Run finished in {time.time() - time_start} seconds')
