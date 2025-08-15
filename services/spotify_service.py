import base64
import requests
import os
from dotenv import load_dotenv
from services.spotify_mood_map import mood_to_playlist  # make sure this import works

# Load variables from .env
load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

def get_spotify_token():
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        raise Exception("Spotify credentials not set")

    auth_string = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }   

    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)

    if response.status_code != 200:
        raise Exception(f"Spotify token error: {response.text}")

    return response.json()["access_token"]

def get_tracks_by_mood(mood: str):
    token = get_spotify_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get playlist name from mood map
    playlist_name = mood_to_playlist.get(mood.lower(), "Chill Hits")

    # Step 1: Search the playlist
    search_url = "https://api.spotify.com/v1/search"
    params = {
        "q": playlist_name,
        "type": "playlist",
        "limit": 5
    }

    search_resp = requests.get(search_url, headers=headers, params=params)
    
    if search_resp.status_code != 200:
        print("Spotify Search Error:", search_resp.text)
        return []
    
    search_data = search_resp.json()
    print("[DEBUG] Spotify Search Response:", search_data)  # 👈 ADD THIS
    
    # Filter out any None items just in case
    playlist_items = [item for item in search_data.get("playlists", {}).get("items", []) if item]

    if not playlist_items:
        print(f"[DEBUG] No playlist found for mood: {mood}, searched: {playlist_name}")
        return []

    playlist_id = playlist_items[0]["id"]

    # Step 2: Get tracks from the playlist
    tracks_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    track_resp = requests.get(tracks_url, headers=headers)
    items = track_resp.json().get("items", [])

    tracks = []
    for item in items[:10]:  # Limit to top 10 tracks
        track = item["track"]
        tracks.append({
            "title": track["name"],
            "artist": ", ".join([a["name"] for a in track["artists"]]),
            "spotify_url": track["external_urls"]["spotify"],
            "preview_url": track.get("preview_url")
        })

    return tracks