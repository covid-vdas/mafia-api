import logging
import shutil

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageSerializer
from .model import Image
from yolov5 import detect
from mafia_api.settings import MEDIA_ROOT, BASE_DIR


# Create your views here.
class ImageView(APIView):

    def post(self, request):
        serializer = ImageSerializer(data=request.data)

        if serializer.is_valid():
            file = serializer.save()
            shutil.rmtree(MEDIA_ROOT / 'detect/exp')
            detect.run(source=MEDIA_ROOT / file.image.name, weights=BASE_DIR / 'yolov5/weights/best-2110-midnight.pt',
                       project=MEDIA_ROOT / 'detect', imgsz=416, conf_thres=0.4)
            return Response({"status": "success", "data": serializer.data}, status=status   .HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
