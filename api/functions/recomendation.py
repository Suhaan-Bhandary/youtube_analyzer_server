# Import the necessary libraries
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Set the API key and define the API service
API_KEY = 'AIzaSyDLzoqpEmFqttF3HDprXGR5eXphBUX5lo4'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

# Define the video link
video_link = 'https://www.youtube.com/watch?v=B1BwqZBy4Zs'

# Extract the video ID from the link
video_id = video_link.split('=')[1]

# Call the videos().list method of the API service to fetch the video details
try:
    video_response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()
except HttpError as error:
    print('An error occurred: %s' % error)
    video_response = None

# Extract the video title and description
if video_response is not None:
    video_title = video_response['items'][0]['snippet']['title']
    video_description = video_response['items'][0]['snippet']['description']

# Call the search().list method of the API service to fetch related videos
try:
    search_response = youtube.search().list(
        part='snippet',
        relatedToVideoId=video_id,
        type='video'
    ).execute()
except HttpError as error:
    print('An error occurred: %s' % error)
    search_response = None

# Create a dataframe to store the related videos and their features
related_videos = pd.DataFrame(columns=['title', 'description'])

# Extract the video titles and descriptions from the search results
if search_response is not None:
    for search_result in search_response.get('items', []):
        title = search_result['snippet']['title']
        description = search_result['snippet']['description']
        related_videos = related_videos.append({'title': title, 'description': description}, ignore_index=True)

# Use TF-IDF vectorizer to extract features from the related videos
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(related_videos['description'])

# Calculate the cosine similarity between the input video and the related videos
input_video_tfidf = tfidf_vectorizer.transform([video_description])
similarity_scores = cosine_similarity(input_video_tfidf, tfidf_matrix)

# Get the top 5 most similar videos
top_indices = similarity_scores[0].argsort()[::-1][:5]
recommended_videos = related_videos.iloc[top_indices]

# Print the recommended videos
print('Recommended Videos:')
for i, video in recommended_videos.iterrows():
    print('%s: %s' % (i+1, video['title']))
