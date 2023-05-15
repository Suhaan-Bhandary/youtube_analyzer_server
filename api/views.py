from django.shortcuts import render

# Create your views here.
import json
from rest_framework.views import Response, APIView, status
from api.functions.youtube_comments import getCommentsFiltered
from api.functions.review import getVideoStatistics
from api.functions.movie_recommendation import getMovieRecommendations


class YoutubeAnalysisView(APIView):
    def post(self, request, format=None):
        youtube_video_url = request.data["youtube_video_url"]
        comment_count = request.data["comment_count"]
        sort_by_most_popular = request.data["sort_by_most_popular"]

        comments = getCommentsFiltered(
            youtube_video_url, comment_count, sort_by_most_popular)
        positive_comments_count = len(comments["positive_comments"])
        negative_comments_count = len(comments["negative_comments"])

        video_statistics = getVideoStatistics(youtube_video_url)

        data = {
            "comments": comments,
            "isVideoGood": (video_statistics["likes"] >= video_statistics["views"] / 1000) and positive_comments_count > negative_comments_count,
            "message": "Successful"
        }

        # TODO: Will return information about the given node
        return Response(data, status=status.HTTP_200_OK)


class MovieRecommendationView(APIView):
    def post(self, request, format=None):
        movieTitle = request.data["movieTitle"]
        movieGenre = request.data["movieGenre"]

        try:
            movies = getMovieRecommendations(movieTitle, movieGenre)
            data = {"movies": movies}
            return Response(data, status=status.HTTP_200_OK)
        except Exception as error:
            print("An error occurred:", error)
            return Response({"message": "Something went Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
