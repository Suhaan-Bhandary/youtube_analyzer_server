from django.urls import path
from api.views import YoutubeAnalysisView

urlpatterns = [
    path('', YoutubeAnalysisView.as_view())
]
