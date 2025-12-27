import kworb_services
import reccobeats_services

from cloudflare_services import cloudflare_manager

MAX_SONGS_PER_QUERY = 50


def run_artist_scrapper():
    songs = kworb_services.get_kworb_songs()
    print(f'Processing {len(songs)} songs')

    cloudflare_manager.bulk_add_to_processing(songs)


def run_recommendation_finder(client):
    artists = cloudflare_manager.get_artists_not_used_for_recommend()
    artists = artists.result[0].results
    if not artists:
        print(f'No artists found to use for recommended')
        return
    
    for row in artists:
        recommended_songs = reccobeats_services.get_recommended([row['origin_song_id']])
        if not recommended_songs:
            continue

        recommended_songs = recommended_songs['content']
        for song in recommended_songs:
            spotify_song_id = song['href']
            song_name = song['trackTitle']
            if not spotify_song_id:
                continue

            spotify_song_id = spotify_song_id[spotify_song_id.rindex('/')+1:]

            song_artists = song['artists']
            for song_artist in song_artists:
                spotify_artist_id = song_artist['href']
                if not spotify_artist_id:
                    continue

                if cloudflare_manager.artist_exists(spotify_artist_id):
                    print(f'Skipping artist "{song_artist["name"]}", Spotify ID already in database')
                    continue
                
                cloudflare_manager.add_artist(spotify_artist_id, song_artist['name'], song_name, spotify_song_id)
                print(f'Added "{song_artist["name"]}" to database')
    
    artist_ids = [artist['spotify_id'] for artist in artists]
    cloudflare_manager.bulk_set_artists_used_for_recommend(artist_ids)


def run():
    run_artist_scrapper()
    run_recommendation_finder()


if __name__ == '__main__':
    run()
