import base64
import glob
import io
import logging
import shutil
import urllib.request
from os import startfile

import cv2.cv2 as cv2
from django.http import StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageSerializer, VideoSerializer, CameraSerializer
from PIL import Image as Img
from .model import Image
from yolov5 import detect
from mafia_api.settings import MEDIA_ROOT, BASE_DIR, DETECT_ROOT


# Create your views here.
class ImageView(APIView):

    def post(self, request):
        shutil.rmtree(MEDIA_ROOT / 'images')
        serializer = ImageSerializer(data=request.data)

        if serializer.is_valid():
            # Save image
            file = serializer.save()

            # Delete previous result
            result_dir = DETECT_ROOT / 'exp'
            shutil.rmtree(result_dir)

            # Detect
            detect.run(source=MEDIA_ROOT / file.image.name, weights=BASE_DIR / 'yolov5/weights/weight.pt',
                       project=DETECT_ROOT, imgsz=[416, 416], conf_thres=0.4)

            # Load detected result
            with open(result_dir / file.image.name[7:], "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())

            return Response({"status": "success", "data": encoded_string}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ImageB64View(APIView):

    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.save()
            result_dir = DETECT_ROOT / 'exp'
            shutil.rmtree(result_dir)

            imgData = file.url.split(',')[1]
            img = Img.open(io.BytesIO(base64.b64decode(imgData)))
            img.save(MEDIA_ROOT / 'images/image.png')
            # Detect
            detect.run(source=MEDIA_ROOT/'images/image.png', weights=BASE_DIR / 'yolov5/weights/weight.pt',
                       project=DETECT_ROOT, imgsz=[416, 416], conf_thres=0.4)

            # Load detected result
            with open(result_dir / 'image.png', "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())

            return Response({"status": "success", "data": encoded_string}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ImageURL(APIView):

    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.save()
            result_dir = DETECT_ROOT / 'exp'
            shutil.rmtree(result_dir)

            urllib.request.urlretrieve(file.url,"temp.png")
            img = Img.open("temp.png")
            img.save(MEDIA_ROOT / 'images/image.png')
            # Detect
            detect.run(source=MEDIA_ROOT/'images/image.png', weights=BASE_DIR / 'yolov5/weights/weight.pt',
                       project=DETECT_ROOT, imgsz=[416, 416], conf_thres=0.4)

            # Load detected result
            with open(result_dir / 'image.png', "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())

            return Response({"status": "success", "data": encoded_string}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class VideoView(APIView):

    def post(self, request):
        shutil.rmtree(MEDIA_ROOT / 'videos')
        serializer = VideoSerializer(data=request.data)

        if serializer.is_valid():
            # Save Video
            file = serializer.save()

            # Delete previous result
            result_dir = DETECT_ROOT / 'exp'
            shutil.rmtree(result_dir)

            # Detect
            detect.run(source=MEDIA_ROOT / file.video.name, weights=BASE_DIR / 'yolov5/weights/weight.pt',
                       project=DETECT_ROOT, imgsz=[416, 416], conf_thres=0.4)

            # Return video url
            return Response({"status": "success", "url": "/media/detect/exp/" + file.video.name[7:]}
                            , status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CameraView(APIView):

    def post(self, request):
        serializer = CameraSerializer(data=request.data)

        if serializer.is_valid():
            # Save Video
            file = serializer.save()
            result_dir = DETECT_ROOT / 'exp'
            shutil.rmtree(result_dir)
            # Detect
            detect.run(source=file.url, weights=BASE_DIR / 'yolov5/weights/weight.pt',
                       project=DETECT_ROOT, imgsz=[416, 416], conf_thres=0.4)

            # Return video url
            return Response({"status": "success", "url": "/media/detect/exp/"}
                            , status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
