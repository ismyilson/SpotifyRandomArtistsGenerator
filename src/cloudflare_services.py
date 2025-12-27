import os

from cloudflare import Cloudflare, APIError


class CloudflareManager:
    API_TOKEN = os.environ.get('CLOUDFLARE_API_TOKEN')

    ACCOUNT_ID = os.environ.get('CLOUDFLARE_ACCOUNT_ID')
    DATABASE_ID = os.environ.get('CLOUDFLARE_DATABASE_ID')

    BULK_MAX_PER_QUERY = 50

    _client: Cloudflare

    def __init__(self):
        self._client = Cloudflare(api_token=self.API_TOKEN)
    
    def _do_query(self, query, params=None):
        try:
            if params:
                params = params if isinstance(params, list) else [params]
                
            result = self._client.d1.database.query(
                account_id=self.ACCOUNT_ID,
                database_id=self.DATABASE_ID,
                sql=query,
                params=params
            )
            return result.result[0].results if len(result.result) > 0 else None
        except APIError as e:
            print(f'Cloudflare API error: {e.message}')
            raise e

    def add_to_processing(self, song):
        query = f'insert into processing (song_fullname) values (?)'
        self._do_query(query, params=song)

    def get_processing(self, limit = 10):
        query = f'select * from processing limit ?'
        return self._do_query(query, params=limit)
    
    def delete_from_processing(self, songs):
        while len(songs):
            data_per_query = self.BULK_MAX_PER_QUERY if len(songs) >= self.BULK_MAX_PER_QUERY else len(songs)
            query = f'delete from processing where song_fullname in ({"?, "*(len(data_per_query)-1)}?)'
            self._do_query(query, params=songs[:data_per_query])
            songs = songs[data_per_query:]

    def bulk_add_to_processing(self, songs):
        while len(songs) > 0:
            data_per_query = self.BULK_MAX_PER_QUERY if len(songs) >= self.BULK_MAX_PER_QUERY else len(songs)
            query = f'insert into processing (song_fullname) values {"(?), "*(data_per_query-1)}(?)'
            self._do_query(query, params=songs[:data_per_query])
            songs = songs[data_per_query:]
    
    def add_artist(self, spotify_id, name, origin_song, origin_song_id):
        query = f'insert into artists (spotify_id, name, origin_song, origin_song_id, used_for_recommended, appeared) values (?, ?, ?, ?, 0, 0)'
        self._do_query(query, params=[spotify_id, name, origin_song, origin_song_id])

    def get_random_non_appeared_artists(self, limit = 15):
        query = f'select spotify_id from artists where appeared = 0 order by random() limit ?'
        return self._do_query(query, limit)

    def get_artists_not_used_for_recommend(self, limit = 10):
        query = f'select * from artists where used_for_recommended = 0 limit ?'
        return self._do_query(query, params=limit)
    
    def bulk_set_artists_used_for_recommend(self, spotify_ids):
        while len(spotify_ids) > 0:
            data_per_query = self.BULK_MAX_PER_QUERY if len(spotify_ids) >= self.BULK_MAX_PER_QUERY else len(spotify_ids)
            query = f'update artists set used_for_recommended = 1 where spotify_id in ({"?, "*(len(data_per_query)-1)}?)'
            self._do_query(query, params=spotify_ids[:data_per_query])
            spotify_ids = spotify_ids[data_per_query:]
    
    def bulk_set_artists_appeared(self, spotify_ids):
        while len(spotify_ids) > 0:
            data_per_query = self.BULK_MAX_PER_QUERY if len(spotify_ids) >= self.BULK_MAX_PER_QUERY else len(spotify_ids)
            query = f'update artists set appeared = 1 where spotify_id in ({"?, "*(len(spotify_ids)-1)}?)'
            self._do_query(query, params=spotify_ids[:data_per_query])
            spotify_ids = spotify_ids[data_per_query:]

    def artist_exists(self, spotify_id):
        query = f'select * from artists where spotify_id = ?'
        result = self._do_query(query, params=spotify_id)
        return len(result) > 0


cloudflare_manager = CloudflareManager()
