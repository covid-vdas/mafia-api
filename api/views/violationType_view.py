from bson.objectid import ObjectId
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, renderers
from api.models.violation_type_model import *
from api.serializers import ViolationTypeSerializer
from api.library.utils import splitHeader

class ViolationTypeView(APIView):
    renderer_classes = [renderers.JSONRenderer]

    def get(self, request: Request):

        if request.headers.get('Authorization') is None:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif request.headers.get('Authorization').find('Bearer') == -1:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        user = splitHeader(request.headers['Authorization'].split(' ')[1])
        if bool(user) is False:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

        violation_types = ViolationType.objects
        violation_type_serializer = ViolationTypeSerializer(violation_types, many=True)
        return Response(violation_type_serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request):

        if request.headers.get('Authorization') is None:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif request.headers.get('Authorization').find('Bearer') == -1:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        user = splitHeader(request.headers['Authorization'].split(' ')[1])
        if bool(user) is False:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

        violation_type_serializer = ViolationTypeSerializer(data=request.data)
        if violation_type_serializer.is_valid():
            violation_type_serializer.save()
        return Response(violation_type_serializer.data, status=status.HTTP_201_CREATED)


class ViolationTypeDetailView(APIView):
    renderer_classes = [renderers.JSONRenderer]

    def get(self, request: Request, id):

        if request.headers.get('Authorization') is None:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif request.headers.get('Authorization').find('Bearer') == -1:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif not ObjectId.is_valid(id):
            return Response({'message': 'Object ID is not valid'}, status=status.HTTP_400_BAD_REQUEST)

        user = splitHeader(request.headers['Authorization'].split(' ')[1])
        if bool(user) is False:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

        violation_type = ViolationType.objects(id=id).first()
        violation_type_serializer = ViolationTypeSerializer(violation_type)
        return Response(violation_type_serializer.data, status=status.HTTP_200_OK)

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
        violation_type = ViolationType.objects(id=id).first()
        violation_type_serializer = ViolationTypeSerializer(violation_type, data=request.data, partial=True)
        if violation_type_serializer.is_valid():
            violation_type.updated_at = datetime.datetime.utcnow()
            violation_type_serializer.save()
            return Response(violation_type_serializer.data, status=status.HTTP_200_OK)
        return Response(violation_type_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

        violation_type = ViolationType.objects(id=id).first()
        violation_type.delete()
        return Response({'message': 'deleted successfully.'}, status=status.HTTP_200_OK)
