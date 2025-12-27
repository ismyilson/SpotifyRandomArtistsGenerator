import spotipy
from spotipy.oauth2 import SpotifyOAuth

from cloudflare_services import cloudflare_manager

PLAYLIST_ID = '1wVT9oPaOYQfLxMMdC2EJg'


def run():
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=['playlist-modify-public']))

    playlist_data = spotify.playlist_items(PLAYLIST_ID)
    track_list = [item['track']['id'] for item in playlist_data['items']]

    if track_list:
        spotify.playlist_remove_all_occurrences_of_items(PLAYLIST_ID, track_list)

    results = cloudflare_manager.get_random_non_appeared_artists(limit = 15)
    if not results:
        print(f'No results')
        return
    
    top_tracks_ids = []
    spotify_ids = []
    for row in results:
        tracks = spotify.artist_top_tracks(row['spotify_id'])['tracks']
        top_tracks_ids.append(tracks[0]['id'])
        spotify_ids.append(row['spotify_id'])
    
    spotify.playlist_add_items(PLAYLIST_ID, top_tracks_ids)
    cloudflare_manager.bulk_set_artists_appeared(spotify_ids)
    print('Done')


if __name__ == '__main__':
    run()
