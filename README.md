# Spotify Daily Random Artists Playlist
I wanted something like Spotify's "Discover Weekly" playlist, but more artist oriented, and as random as possible, so that's where this project comes from.

Since there's no way to get a random artist from Spotify, I've built my own database based on a little algorithm I've made to try to get as many artists as possible (see [scripts](https://github.com/ismyilson/SpotifyRandomArtistsGenerator/tree/main/src/scripts)). I've used [Spotify's API](https://developer.spotify.com/documentation/web-api), aswell as [Reccobeats](https://reccobeats.com/).

- `processor.py` runs once every 15 minutes.
- `artist_discoverer.py` runs once every day.
- `spotify_playlist_maker.py` runs once every day.

You can check out and follow the playlist [here](https://open.spotify.com/playlist/1wVT9oPaOYQfLxMMdC2EJg?si=c94d1fb2fd0548d7).
