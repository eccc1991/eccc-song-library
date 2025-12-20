from ytmusicapi import YTMusic
import pandas as pd
import time

yt = YTMusic()

# 1. 搜尋歌手
artist_search_name = "HKACM" 
search_results = yt.search(artist_search_name, filter="artists")
artist_id = search_results[0]['browseId']
artist_data = yt.get_artist(artist_id)

all_song_data = []
sections = [artist_data.get('albums', {}), artist_data.get('singles', {})]

for section in sections:
    if 'results' in section:
        for item in section['results']:
            album_id = item['browseId']
            album_details = yt.get_album(album_id)
            album_name = album_details['title']
            year = album_details.get('year', 'N/A')
            
            for track in album_details['tracks']:
                lyrics_text = "Lyrics not found"
                try:
                    watch_playlist = yt.get_watch_playlist(track['videoId'])
                    lyrics_id = watch_playlist.get('lyrics')
                    if lyrics_id:
                        lyrics_text = yt.get_lyrics(lyrics_id)['lyrics']
                    time.sleep(0.5)
                except:
                    pass
                    
                all_song_data.append({
                    "Artist": artist_search_name,
                    "Song Title": track['title'],
                    "Album": album_name,
                    "Year": year,
                    "Lyrics": lyrics_text,
                    "Link": f"https://music.youtube.com/watch?v={track['videoId']}"
                })

# 2. 儲存
df = pd.DataFrame(all_song_data)
df = df.drop_duplicates(subset=['Song Title', 'Artist'])
df.to_csv("eccc-song-library-2026.csv", index=False, encoding='utf-8-sig')
print("Successfully updated CSV!")
