import requests
from bs4 import BeautifulSoup
import urllib.request
import re
import yt_dlp
import platform
from pathlib import Path
import os

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

# Function to fetch song details from a Spotify track URL
def get_song_details_from_url(track_url):
    """Fetch track details (song name, artist) from the Spotify track URL."""
    try:
        # Send a request to the track URL
        response = requests.get(track_url)
        
        if response.status_code != 200:
            print(f"Error: Unable to fetch details for {track_url}")
            return None
        
        # Parse the page HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the song name, artist, and album
        song_name = soup.find('title').get_text(strip=True) if soup.find('title') else 'Unknown Song'

        # Print out the extracted details
        print(f"Song: {song_name}")

        
        return f"{song_name}"
    
    except Exception as e:
        print(f"Error while scraping track details for {track_url}: {e}")
        return None

# Function to fetch song link from search results on YouTube
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

# Function to scrape and extract track URLs from meta tags
def get_track_urls_from_page(playlist_url):
    """Extracts track URLs from a playlist or page containing meta tags with Spotify track links."""
    response = requests.get(playlist_url)
    
    if response.status_code != 200:
        print("Error: Unable to fetch playlist page.")
        return []

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract all track URLs from the meta tags with name="music:song"
    track_urls = []
    for meta_tag in soup.find_all('meta', {'name': 'music:song'}):
        track_url = meta_tag.get('content')
        if track_url:
            track_urls.append(track_url)
    
    return track_urls

def main():
    # Input the URL containing the meta tags with track links
    playlist_link = input("Enter the URL containing the track links: ")

    # Step 1: Extract track URLs from the page
    track_urls = get_track_urls_from_page(playlist_link)

    if not track_urls:
        return

    # Step 2: Fetch details for each track
    for track_url in track_urls:
        song_details = get_song_details_from_url(track_url)
        
        if song_details:
            song_link = get_song_link(song_details)
            if song_link:
                print(f"Downloading: {song_details}")
                download_video(song_link)

if __name__ == "__main__":
    main()
