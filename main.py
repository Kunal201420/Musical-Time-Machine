import billboard
import spotipy
from spotipy import SpotifyOAuth
import os


#---------------------Configuration------------------------
SPOTIFY_ID = os.getenv('SPOTIFY_ID')
SPOTIFY_SECRET = os.getenv('SPOTIFY_SECRET')
REDIRECT_URL = os.getenv('REDIRECT_URL')

DATE = input("Enter the date to generate 100 hot songs list: (YYYY-MM-DD)format\n")

#---------------------Authenticate with Spotify------------------------
scope= "playlist-modify-private"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_ID,
        client_secret=SPOTIFY_SECRET,
        redirect_uri=REDIRECT_URL,
        scope=scope
    )
)

#---------------------Get hot 100 songs------------------------
print(f"Fetching hot 100 songs for {DATE}...")
chart = billboard.ChartData('hot-100',date=DATE)
songs = [(entry.title , entry.artist) for entry in chart]
print(f"Retrieved {len(songs)} songs. ")

#---------------------Find songs on Spotify------------------------
track_uris = []
for title, artist in songs:
    query = f"track:{title} artist:{artist}"
    result = sp.search(q=query, type='track', limit=1)
    tracks = result.get("tracks",{}).get("items",[])
    if tracks:
        uri = tracks[0]['uri']
        track_uris.append(uri)
        print(f"🎶 Found {title} - {artist}")
    else:
        print(f"❌ Not found {title} - {artist}")

print(f"Found {len(track_uris)}/{len(songs)} on Spotify.")

#---------------------Create Playlist------------------------
user_id = sp.current_user()['id']
playlist_name = f"Hot 100 - {DATE}"
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
print(f"\n🎶 Created playlist: {playlist['external_urls']['spotify']}")

#---------------------Add tracks to playlist------------------------
for i in range(0, len(track_uris), 100):
    sp.playlist_add_items(playlist["id"], track_uris[i:i+100])

print(f"✅ Added {len(track_uris)} tracks to '{playlist_name}'!")