from django.urls import path
from .views import *
from .views import getAllCamera, getAllArea, getAllManager

urlpatterns = [
    # path('image/', ImageView.as_view()),
    # path('imageb64/', ImageB64View.as_view()),
    # path('imageurl/', ImageURL.as_view()),
    # path('video/', VideoView.as_view()),
    path('url/', CameraView.as_view()),
    path('user/', UserView.as_view()),
    path('user/getAllManager/', getAllManager),
    path('user/<slug:id>/', UserDetailView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('role/', RoleView.as_view()),
    path('role/<slug:id>/', RoleDetailView.as_view()),
    path('area/', AreaView.as_view()),
    path('area/getAllArea/', getAllArea),
    path('area/<slug:id>/', AreaDetailView.as_view()),
    path('camera/', CameraView.as_view()),
    path('camera/getAllCamera/<slug:area_id>/', getAllCamera),
    path('camera/<slug:id>/', CameraDetailView.as_view()),
    path('objectinformation/', ObjectInformationView.as_view()),
    path('objectinformation/<slug:id>/', ObjectInformationDetailView.as_view()),
    path('violation/', ViolationView.as_view()),
    path('violation/<slug:id>/', ViolationDetailView.as_view()),
    path('violationtype/', ViolationTypeView.as_view()),
    path('violationtype/<slug:id>/', ViolationTypeDetailView.as_view()),
    path('image/', ImageView.as_view()),
    path('image/<slug:id>/', ImageDetailView.as_view()),
]