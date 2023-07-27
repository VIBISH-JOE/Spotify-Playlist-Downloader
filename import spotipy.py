
import spotipy,csv,pafy,re
import urllib.request
from youtubesearchpython import VideosSearch
from spotipy.oauth2 import SpotifyClientCredentials


auth_manager = SpotifyClientCredentials(client_id="62eb3be2084846a5a27e6d6b293ecd0f",client_secret="7b23ef02ab1749d4864b8a6c6b95d5cf"
)
sp = spotipy.Spotify(auth_manager=auth_manager)


#playlist=input("playlist link?")
songs=sp.playlist("https://open.spotify.com/playlist/7szrhodad8xEBkmLw9zjjg?si=836a03316dcb45df")

no_of_songs=songs["tracks"]["total"]

items=songs['tracks']['items']
i=0
str=''
while i<no_of_songs:
    str=str+items[i]['track']['name']+','
    i+=1
print(str)
song_name=str.split(',')
song_name.pop()

for meow in song_name:
    hello=meow.split()
    newstr=''
    for h in hello:   
        newstr=newstr+h+'+'
    length=len(newstr)
    newstr2=newstr[:length-1]
    link='https://www.youtube.com/results?search_query='+newstr2
    #print(link)
    html=urllib.request.urlopen(link)
    video_ids= re.findall(r"watch\?v=(\S{11})",html.read().decode())
    #print('https://www.youtube.com/watch?v='+video_ids[0])
    song_link='https://www.youtube.com/watch?v='+video_ids[0]
    print(song_link)
    video = pafy.new(song_link)
    print("Video Title:", video.title)
    print("Duration:", video.duration)
    print("Author:", video.author)

    #streams = video.streams
    #best_stream = video.getbest()
    #best_stream.download(filepath="D:\Videos")
