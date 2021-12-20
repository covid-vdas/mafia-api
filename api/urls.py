from django.urls import path
from .views import ImageView, ImageB64View, ImageURL, VideoView, CameraView

urlpatterns = [
    path('image/', ImageView.as_view()),
    path('imageb64/', ImageB64View.as_view()),
    path('imageurl/', ImageURL.as_view()),
    path('video/', VideoView.as_view()),
    path('url/', CameraView.as_view())
]