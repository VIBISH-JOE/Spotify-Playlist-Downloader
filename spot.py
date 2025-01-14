import spotipy
import urllib.request
import re
import yt_dlp
from spotipy.oauth2 import SpotifyClientCredentials
import os
import platform
from pathlib import Path

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

def main():
    # Spotify authentication
    auth_manager = SpotifyClientCredentials(client_id="62eb3be2084846a5a27e6d6b293ecd0f", client_secret="7b23ef02ab1749d4864b8a6c6b95d5cf")
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Get playlist URL
    playlist = input("Enter playlist link: ")
    songs = sp.playlist(playlist)
    no_of_songs = songs["tracks"]["total"]
    items = songs['tracks']['items']

    song_names = []
    for item in items:
        song_names.append(item['track']['name'])

    # Display the list of songs
    print("Songs found in playlist:")
    print(', '.join(song_names))

    # Process each song
    for song in song_names:
        song_link = get_song_link(song)
        if song_link:
            print(f"Downloading: {song}")
            download_video(song_link)

if __name__ == "__main__":
    main()
