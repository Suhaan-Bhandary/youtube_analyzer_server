from django.urls import path
from api.views import YoutubeAnalysisView, MovieRecommendationView

urlpatterns = [
    path('', YoutubeAnalysisView.as_view()),
    path('movie', MovieRecommendationView.as_view()),
]
