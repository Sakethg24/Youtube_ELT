import requests
import json
import os 
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
handle = "casey"

max_results = 50

def get_playlist_id():
    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={handle}&key={API_KEY}"

        response = requests.get(url)
        response.raise_for_status()

        data = response.json()


        channel_items = data["items"][0]
        channel_playlistID = channel_items["contentDetails"]["relatedPlaylists"]

        return channel_playlistID
    
    except requests.exceptions.RequestException as e:
        raise e 
    




def get_video_ids(playlistID):
    video_ids =[]

    pageToken = None 
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_results}&playlistId={playlistID}&key={API_KEY}"

    try:
        while True:
            url = base_url
            if pageToken:
                url += f"&pageToken={pageToken}"
            
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            
            for item in data.get('items',[]):
                video_id =item['contentDetails']['videoId']
                video_ids.append(video_id)

            pageToken = data.get('nextPageToken')

            if not pageToken:
                break
        return video_ids
    except requests.exceptions.RequestException as e:
        raise e 


if __name__ == "__main__":
    playlistID = get_playlist_id()["uploads"]
    print(get_video_ids(playlistID))