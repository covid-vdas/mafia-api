from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, renderers
from api.models.violation_model import *
from api.serializers import ViolationSerializer
from api.library.utils import splitHeader
from bson import ObjectId


class ViolationView(APIView):
    renderer_classes = [renderers.JSONRenderer]

    def get(self, request: Request):

        if request.headers.get('Authorization') is None:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif request.headers.get('Authorization').find('Bearer') == -1:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        user = splitHeader(request.headers['Authorization'].split(' ')[1])
        if bool(user) is False:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

        violations = Violation.objects
        violation_serializer = ViolationSerializer(violations, many=True)
        return Response(violation_serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request):

        if request.headers.get('Authorization') is None:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif request.headers.get('Authorization').find('Bearer') == -1:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        user = splitHeader(request.headers['Authorization'].split(' ')[1])
        if bool(user) is False:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

        violation_serializer = ViolationSerializer(data=request.data)
        if violation_serializer.is_valid():
            violation_serializer.save()
            return Response(violation_serializer.data, status=status.HTTP_200_OK)
        return Response(violation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViolationDetailView(APIView):
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

        violation = Violation.objects(id=id).first()
        camera_serializer = ViolationSerializer(violation)
        return Response(camera_serializer.data, status=status.HTTP_200_OK)

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

        violation = Violation.objects(id=id).first()
        violation_serializer = ViolationSerializer(violation, data=request.data, partial=True)
        return Response(violation_serializer.data, status=status.HTTP_200_OK)

    # def delete(self, request: Request, id):
    #
    #     if request.headers.get('Authorization') is None:
    #         return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
    #     elif request.headers.get('Authorization').find('Bearer') == -1:
    #         return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
    #     elif not ObjectId.is_valid(id):
    #         return Response({'message': 'Object ID is not valid'}, status=status.HTTP_400_BAD_REQUEST)
    #
    #     user = splitHeader(request.headers['Authorization'].split(' ')[1])
    #     if bool(user) is False:
    #         return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
    #
    #     violation = Violation.objects(id=id).first()
    #     violation.delete()
    #     return Response({'message': 'deleted successfully.'}, status=status.HTTP_200_OK)
