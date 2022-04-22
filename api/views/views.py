# import base64
# import io
# import shutil
# import urllib.request
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from api.serializers import *
# from PIL import Image as Img
# from yolov5 import detect
# from mafia_api.settings import MEDIA_ROOT, BASE_DIR, DETECT_ROOT
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')
