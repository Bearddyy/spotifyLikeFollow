# Simply iterate through all the artists in the liked songs playlist and follow them
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import tqdm

# Spotify API credentials
with open('credentials.json') as f:
    credentials = json.load(f)

client_id = credentials['client_id']
client_secret = credentials['client_secret']

scope = "user-follow-modify,user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri="http://localhost:8080", scope=scope))



artists_to_follow = []

offset = 0


while True:
    try:
        # Get all the liked songs
        results = sp.current_user_saved_tracks(limit=50, offset=offset)
        for idx, item in enumerate(results['items']):
            track = item['track']
            artist = track['artists'][0]
            artist_id = artist['id']
            artists_to_follow.append(artist_id)
        
        offset = offset + 50
        print("Artists So Far: " + str(offset), end='\r')

        # If we got less than 50 results, we're done
        if len(results['items']) != 50:
            break
    except:
        break

# Remove duplicates
artists_to_follow = list(set(artists_to_follow))

print("Found " + str(len(artists_to_follow)) + " artists to follow")

progress_bar = tqdm.tqdm(total=len(artists_to_follow), desc="Following Artists")
# Follow all the artists in groups of 50
for i in range(0, len(artists_to_follow), 50):
    sp.user_follow_artists(artists_to_follow[i:i+50])
    progress_bar.update(50)
progress_bar.close()

print("Done! Followed " + str(len(artists_to_follow)) + " artists")