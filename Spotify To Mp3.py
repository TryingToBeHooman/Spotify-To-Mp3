import threading, spotipy, string, random, os
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch
from pytube import YouTube

os.system('cls')

CLIENT_ID = ''
CLIENT_SECRET = ''

def remove_forbidden_chars(pp):
    forbidden_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in forbidden_chars:
        pp = pp.replace(char, '')
    if pp == '':
        for i in range(15):
            pp += random.choice(string.ascii_letters)
    return pp

client_credentials__manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials__manager)

playlist_link = input('Spotify Playlist Link >>>  ')

playlist_parts = playlist_link.split('/')
playlist_id = playlist_parts[-1].split('?')[0]

results = sp.playlist_tracks(playlist_id)

playlist_details = sp.playlist(playlist_id)
playlist_name = playlist_details['name']

folder_path = f'./{remove_forbidden_chars(playlist_name)}'

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

def download_track(track):
    song_name = remove_forbidden_chars(track['track']['name'])
    artists = [artists['name'] for artists in track['track']['artists']]
    artists_str = ', '.join(artists)

    path  = os.path.join(folder_path, remove_forbidden_chars(song_name)+'.mp3')

    if not os.path.exists(path):
        youtube_search = VideosSearch(f'{song_name} By {artists_str} audio', limit=1)
        link = youtube_search.result()['result'][-1]['link']
        yt = YouTube(link)
        video = yt.streams.filter(only_audio=True).first()

        video.download(filename=song_name+'.mp3', output_path=folder_path)

threads = []
for track in results['items']:
    thread = threading.Thread(target=download_track, args=(track,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
