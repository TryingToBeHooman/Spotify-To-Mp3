import spotipy, os, shutil
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch
from pytube import YouTube
os.system('cls')

CLIENT_ID = ''
CLIENT_SECRET = ''

forbidden_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']

client_credentials__manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials__manager)

playlist_link = input('Spotify Playlist Link >>>  ')

playlist_parts = playlist_link.split('/')
playlist_id = playlist_parts[-1].split('?')[0]

results = sp.playlist_tracks(playlist_id)

playlist_details = sp.playlist(playlist_id)
playlist_name = playlist_details['name']

folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), playlist_name)
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
else:
    shutil.rmtree(folder_path)

for track in results['items']:
    track_info = track['track']
    song_name = track_info['name']

    for char in forbidden_chars:
        song_name = song_name.replace(char, '')

    artists = [artists['name'] for artists in track_info['artists']]
    artists_str = ', '.join(artists)

    youtube_search = VideosSearch(f'{song_name} By {artists_str} audio', limit=1)
    link = youtube_search.result()['result'][-1]['link']

    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    dest = folder_path
    video.download(filename=song_name+'.mp3',output_path=dest)
