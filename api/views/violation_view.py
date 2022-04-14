from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, renderers
from api.models.violation_model import *
from api.serializers import ViolationSerializer
from api.library.utils import splitHeader
from bson import ObjectId
from api.models.camera_model import *


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

        for violation in violation_serializer.data:
            dynamically_camera(violation)

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

        try:
            violation = Violation.objects(id=id).first()
            camera_serializer = ViolationSerializer(violation)
            return Response(camera_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)

        return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)


    # def patch(self, request: Request, id):
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
    #     violation_serializer = ViolationSerializer(violation, data=request.data, partial=True)
    #     return Response(violation_serializer.data, status=status.HTTP_200_OK)

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


@api_view(['GET'])
def getAllViolation(request: Request, camera_id):

    if request.headers.get('Authorization') is None:
        return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
    elif request.headers.get('Authorization').find('Bearer') == -1:
        return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
    elif not ObjectId.is_valid(camera_id):
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

        list_violation_by_camera = Violation.objects(camera_id=camera_id).skip(offset).limit(int(limit_record))
        list_violation_by_camera_serializer = ViolationSerializer(list_violation_by_camera, many=True)

        for violation in list_violation_by_camera_serializer.data:
            dynamically_camera(violation)

        return Response(list_violation_by_camera_serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': 'query page or limit record invalid'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)


def dynamically_camera(violation_serializer):
    """
        @ user_serializer: OrderedList

        transforms role_id to store id and name

        return OrderedList
    """
    try:
        camera = Camera.objects(id=ObjectId(violation_serializer['camera_id'])).first()
        violation_serializer['camera_id'] = {
            'id': str(violation_serializer['camera_id']),
            'name': str(camera.name)
        }
    except Exception as e:
        print(e)
    return violation_serializer

