import requests

from bs4 import BeautifulSoup


URL_KWORB_GLOBAL_ITUNES = 'https://kworb.net/ww/'
URL_KWORB_GLOBAL_APPLE_MUSIC = 'https://kworb.net/apple_songs/'
URL_KWORB_GLOBAL_SPOTIFY = 'https://kworb.net/spotify/country/global_weekly.html'
URL_KWORB_CHARTS = 'https://kworb.net/charts/'

SONG_CELL_INDEX = 2


def _kworb_worldwide_section_table_scrapper(soup):
    table = soup.find('table')

    if not table:
        return []
    
    songs = set()
    for element in table.tbody.find_all('tr'):
        cells = element.find_all('td')
        songname = cells[SONG_CELL_INDEX].find('div').get_text()
        
        songs.add(songname)
    
    return songs


def get_itunes_songs():
    r = requests.get(URL_KWORB_GLOBAL_ITUNES)
    soup = BeautifulSoup(r.content, 'html.parser', from_encoding='utf-8')
    return _kworb_worldwide_section_table_scrapper(soup)


def get_apple_music_songs():
    r = requests.get(URL_KWORB_GLOBAL_APPLE_MUSIC)
    soup = BeautifulSoup(r.content, 'html.parser', from_encoding='utf-8')
    return _kworb_worldwide_section_table_scrapper(soup)


def get_spotify_songs():
    r = requests.get(URL_KWORB_GLOBAL_SPOTIFY)
    soup = BeautifulSoup(r.content, 'html.parser', from_encoding='utf-8')
    return _kworb_worldwide_section_table_scrapper(soup)


def get_charts_songs():
    r = requests.get(URL_KWORB_CHARTS)
    soup = BeautifulSoup(r.content, 'html.parser', from_encoding='utf-8')

    # There's currently 2 tables, one for "main countries" and another for "other countries"
    songs = set()
    tables = soup.find_all('table')
    for table in tables:
        for element in table.tbody.find_all('tr'):
            cells = element.find_all('td')
            for cell in cells:
                div = cell.find('div')
                if not div:
                    continue

                link_ref = div.find('a')
                if not link_ref:
                    continue

                songname = link_ref.get_text()
                songs.add(songname)

    return songs


def get_kworb_songs():
    songs = set()
    songs.update(get_itunes_songs())
    songs.update(get_apple_music_songs())
    songs.update(get_spotify_songs())
    songs.update(get_charts_songs())

    return list(songs)
