from django.urls import path
from .views import ImageView, VideoView, CameraView

urlpatterns = [
    path('image/', ImageView.as_view()),
    path('video/', VideoView.as_view()),
    path('url/', CameraView.as_view())
]