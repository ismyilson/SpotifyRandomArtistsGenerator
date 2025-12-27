import requests


def get_recommended(from_songs, amount=25):
    payload  = {
        'size': amount,
        'seeds': from_songs,
    }
    r = requests.get('https://api.reccobeats.com/v1/track/recommendation', payload)
    if r.status_code != 200:
        return None

    return r.json()
