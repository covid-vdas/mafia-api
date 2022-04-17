from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, renderers
from api.models.camera_model import *
from api.serializers import CameraSerializer
from api.library.utils import splitHeader
from bson import ObjectId
from api.models.area_model import Area
from api.models.role_model import Role



class CameraView(APIView):
    renderer_classes = [renderers.JSONRenderer]

    def get(self, request: Request):
        if request.headers.get('Authorization') is None:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif request.headers.get('Authorization').find('Bearer') == -1:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        user = splitHeader(request.headers['Authorization'].split(' ')[1])
        if bool(user) is False:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user_role_login = Role.objects(id=user.role_id).first()

            if user_role_login.name == 'admin':
                cameras = Camera.objects
                camera_serializer = CameraSerializer(cameras, many=True)
                return Response(camera_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)

        return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        if request.headers.get('Authorization') is None:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif request.headers.get('Authorization').find('Bearer') == -1:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        user = splitHeader(request.headers['Authorization'].split(' ')[1])
        if bool(user) is False:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user_role_login = Role.objects(id=user.role_id).first()
            if user_role_login.name == 'staff':
                return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

            camera_serializer = CameraSerializer(data=request.data)
            if camera_serializer.is_valid():
                camera_serializer.save()
                return Response(camera_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)

        return Response(camera_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CameraDetailView(APIView):
    renderer_classes = [renderers.JSONRenderer]

    def get(self, request, id):
        if request.headers.get('Authorization') is None:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif request.headers.get('Authorization').find('Bearer') == -1:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif not ObjectId.is_valid(id):
            return Response({'message': 'Object ID is not valid'}, status=status.HTTP_400_BAD_REQUEST)

        user = splitHeader(request.headers['Authorization'].split(' ')[1])
        if bool(user) is False:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            camera = Camera.objects(id=id).first()
            if camera is not None:
                camera_serializer = CameraSerializer(camera)
                return Response(camera_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Camera not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(camera_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request: Request, id):

        if request.headers.get('Authorization') is None:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif request.headers.get('Authorization').find('Bearer') == -1:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif not ObjectId.is_valid(id):
            return Response({'message': 'Object ID is not valid'}, status=status.HTTP_400_BAD_REQUEST)

        user = splitHeader(request.headers['Authorization'].split(' ')[1])
        if bool(user) is False:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user_role_login = Role.objects(id=user.role_id).first()
            if user_role_login.name == 'staff':
                return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

            camera = Camera.objects(id=id).first()
            camera_serializer = CameraSerializer(camera, data=request.data, partial=True)
            if camera_serializer.is_valid():
                camera.updated_at = datetime.datetime.utcnow()
                camera_serializer.save()
                return Response(camera_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
        return Response(camera_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, id):
        if request.headers.get('Authorization') is None:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif request.headers.get('Authorization').find('Bearer') == -1:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif not ObjectId.is_valid(id):
            return Response({'message': 'Object ID is not valid'}, status=status.HTTP_400_BAD_REQUEST)

        user = splitHeader(request.headers['Authorization'].split(' ')[1])
        if bool(user) is False:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user_role_login = Role.objects(id=user.role_id).first()
            if user_role_login.name == 'staff':
                return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

            # handle logic
            camera = Camera.objects(id=id).first()
            area = Area.objects(id=camera.area_id).first()
            if user_role_login.name == 'manager' and str(user.id) != area.managed_manager:
                return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
            camera.delete()
            return Response({'message': 'deleted successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': 'object not found.'}, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['GET'])
def getAllCamera(request: Request, area_id):
    if request.headers.get('Authorization') is None:
        return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
    elif request.headers.get('Authorization').find('Bearer') == -1:
        return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
    elif not ObjectId.is_valid(area_id):
        return Response({'message': 'Object ID is not valid'}, status=status.HTTP_400_BAD_REQUEST)

    user = splitHeader(request.headers['Authorization'].split(' ')[1])
    if bool(user) is False:
        return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        offset = 0
        limit_record = 0
        page_number = 1

        if bool(request.query_params.get('limit')) is True:
            limit_record = request.query_params.get('limit')
            if not limit_record.isdigit():
                return Response({'message': 'limit record invalid'}, status=status.HTTP_400_BAD_REQUEST)

        if bool(request.query_params.get('page')) is True:
            page_number = request.query_params.get('page')
            if page_number.isdigit():
                offset = (int(page_number) - 1) * int(limit_record)
            else:
                return Response({'message': 'query page invalid'}, status=status.HTTP_400_BAD_REQUEST)

        user_role_login = Role.objects(id=user.role_id).first()

        if user_role_login.name == 'manager':
            area = Area.objects(id=area_id).first()
            print(area.managed_manager)
            if area.managed_manager != str(user.id):
                return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif user_role_login.name == 'staff':
            area = Area.objects(id=area_id).first()
            if area.managed_staff != str(user.id):
                return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

        list_camera = Camera.objects(area_id=area_id).skip(offset).limit(int(limit_record))
        list_camera_serializer = CameraSerializer(list_camera, many=True)
        return Response(list_camera_serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': 'query page or limit record invalid'}, status=status.HTTP_400_BAD_REQUEST)