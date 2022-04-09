from bson import ObjectId
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, renderers
from api.models.area_model import *
from api.library.utils import splitHeader
from api.models.object_information import ObjectClass
from api.serializers import ObjectClassSerializer


class ObjectClassView(APIView):
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
            object_class = ObjectClass.objects

            object_class_serializer = ObjectClassSerializer(object_class, many=True)
            return Response(object_class_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)

    def post(self, request):
        if request.headers.get('Authorization') is None:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif request.headers.get('Authorization').find('Bearer') == -1:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        user = splitHeader(request.headers['Authorization'].split(' ')[1])
        if bool(user) is False:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

        object_class_serializer = ObjectClassSerializer(data=request.data)
        if object_class_serializer.is_valid():
            object_class_serializer.save()
            return Response(object_class_serializer.data, status=status.HTTP_200_OK)
        return Response(object_class_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObjectClassDetailView(APIView):
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

        object_class = ObjectClass.objects(id=id).first()
        object_class_serializer = ObjectClassSerializer(object_class)
        return Response(object_class_serializer.data, status=status.HTTP_200_OK)

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

        object_class = ObjectClass.objects(id=id).first()
        object_class_serializer = ObjectClassSerializer(object_class, data=request.data, partial=True)
        if object_class_serializer.is_valid():
            object_class.object_class_serializer = datetime.datetime.utcnow()
            object_class_serializer.save()
            return Response(object_class_serializer.data, status=status.HTTP_200_OK)
        return Response(object_class_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        object_class = ObjectClass.objects(id=id).first()
        object_class.delete()
        return Response({'message': 'deleted successfully.'}, status=status.HTTP_200_OK)
