from datetime import datetime
from bson import ObjectId
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, renderers
from api.models.role_model import Role
from api.serializers import RoleSerializer
from api.library.utils import splitHeader
import datetime


class RoleView(APIView):
    renderer_classes = [renderers.JSONRenderer]

    def get(self, request: Request):

        if request.headers.get('Authorization') is None:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif request.headers.get('Authorization').find('Bearer') == -1:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        user = splitHeader(request.headers['Authorization'].split(' ')[1])
        if bool(user) is False:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        roles = Role.objects
        role_serializer = RoleSerializer(roles, many=True)
        return Response(role_serializer.data, status=status.HTTP_200_OK)


class RoleDetailView(APIView):
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

        role = Role.objects(id=id).first()
        role_serializer = RoleSerializer(role)
        return Response(role_serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):

        if request.headers.get('Authorization') is None:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif request.headers.get('Authorization').find('Bearer') == -1:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif not ObjectId.is_valid(id):
            return Response({'message': 'Object ID is not valid'}, status=status.HTTP_400_BAD_REQUEST)

        user = splitHeader(request.headers['Authorization'].split(' ')[1])
        if bool(user) is False:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

        role = Role.objects(id=id).first()
        role_serializer = RoleSerializer(role, data=request.data, partial=True)

        if role_serializer.is_valid():
            role.updated_at = datetime.datetime.utcnow()
            role_serializer.save()
            return Response(role_serializer.data, status=status.HTTP_200_OK)
        return Response(role_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
