from django.urls import path
from .views import ImageView

urlpatterns = [
    path('image/', ImageView.as_view())
]