import base64
import glob
import logging
import shutil

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageSerializer
from PIL import Image as Img
from .model import Image
from yolov5 import detect
from mafia_api.settings import MEDIA_ROOT, BASE_DIR, DETECT_ROOT


# Create your views here.
class ImageView(APIView):

    def post(self, request):
        serializer = ImageSerializer(data=request.data)

        if serializer.is_valid():
            # Save image
            file = serializer.save()

            # Delete previous result
            result_dir = DETECT_ROOT / 'exp'
            shutil.rmtree(result_dir)

            # Detect
            detect.run(source=MEDIA_ROOT / file.image.name, weights=BASE_DIR / 'yolov5/weights/best-2110-midnight.pt',
                       project=DETECT_ROOT, imgsz=416, conf_thres=0.4)

            # Load detected result
            with open(result_dir / file.image.name[7:], "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())

            return Response({"status": "success", "data": encoded_string}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
