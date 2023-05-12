

from googleapiclient.discovery import build
import os

def getVideoStatistics(youtube_video_url):
    # Define the YouTube API client
    api_key = os.getenv('API_KEY') 
    youtube = build('youtube', 'v3', developerKey=api_key)

    # good link ZyKwNDV_9M4
    # bad link n9XX_zz3bi8
    video_id = youtube_video_url.split('=')[1]

    # Use the YouTube API to retrieve the video statistics
    video_response = youtube.videos().list(
        part='statistics',
        id=video_id
    ).execute()

    # Get the number of views and likes for the video
    views = int(video_response['items'][0]['statistics']['viewCount'])
    likes = int(video_response['items'][0]['statistics']['likeCount'])

    return {
        "views": views,
        "likes": likes,
    }
