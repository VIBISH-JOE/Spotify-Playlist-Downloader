import requests
import urllib.request
import re
import yt_dlp
import platform
from pathlib import Path

# Function to get default Downloads folder path
def get_downloads_folder():
    """Returns the path to the default Downloads folder."""
    if platform.system() == "Windows":
        return str(Path(os.environ["USERPROFILE"]) / "Downloads")
    elif platform.system() == "Darwin":
        return str(Path.home() / "Downloads")
    elif platform.system() == "Linux":
        return str(Path.home() / "Downloads")
    else:
        raise OSError("Unsupported Operating System")

# Function to download video using yt-dlp
def download_video(url):
    # Get the default Downloads folder path
    download_path = get_downloads_folder()

    # Set options for yt-dlp
    ydl_opts = {
        'outtmpl': f'{download_path}/%(title)s.%(ext)s',
        'format': 'bv*[height<=1080]+ba/b',  # Download the best quality available
    }

    try:
        # Download video using yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Download successful! File saved to: {download_path}")
    except Exception as e:
        print(f"Error: {e}")

# Function to fetch YouTube video link based on song name
def get_song_link(song_name):
    # Replace spaces with '+' for the YouTube search query
    query = '+'.join(song_name.split())
    url = f'https://www.youtube.com/results?search_query={query}'
    
    try:
        # Open the YouTube search results page
        html = urllib.request.urlopen(url)
        # Extract the video ID using regex
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        
        if video_ids:
            # Return the first video found
            return f'https://www.youtube.com/watch?v={video_ids[0]}'
        else:
            print(f"No YouTube video found for: {song_name}")
            return None
    except Exception as e:
        print(f"Error during YouTube search for {song_name}: {e}")
        return None

# Function to get playlist details from Spotify (public playlist, no authentication)
def get_playlist_details(playlist_url):
    """Returns details of a public Spotify playlist."""
    # Extract playlist ID from the URL
    playlist_id = playlist_url.split("/")[-1].split("?")[0]

    # Spotify API URL for fetching playlist details
    api_url = f"https://api.spotify.com/v1/playlists/{playlist_id}"

    # Send GET request to Spotify API without authentication
    response = requests.get(api_url)

    if response.status_code == 200:
        # Parse JSON response
        playlist_data = response.json()

        # Extract details from the response
        playlist_name = playlist_data["name"]
        playlist_owner = playlist_data["owner"]["display_name"]
        total_tracks = playlist_data["tracks"]["total"]
        description = playlist_data["description"]

        # Display details
        print(f"Playlist Name: {playlist_name}")
        print(f"Owner: {playlist_owner}")
        print(f"Total Tracks: {total_tracks}")
        print(f"Description: {description}")
        print("\nTrack List:")

        # Extract track details
        song_names = []
        for item in playlist_data["tracks"]["items"]:
            track_name = item["track"]["name"]
            artist_name = item["track"]["artists"][0]["name"]
            song_names.append(f"{track_name} by {artist_name}")
            print(f" - {track_name} by {artist_name}")

        return song_names
    else:
        print("Error: Unable to fetch playlist details. Status code:", response.status_code)
        return []

def main():
    # Input Spotify playlist link
    playlist_link = input("Enter the Spotify playlist link: ")

    # Get the song list from the Spotify playlist (public)
    song_names = get_playlist_details(playlist_link)

    if not song_names:
        return

    # Process each song in the playlist
    for song in song_names:
        song_link = get_song_link(song)
        if song_link:
            print(f"Downloading: {song}")
            download_video(song_link)

if __name__ == "__main__":
    main()
