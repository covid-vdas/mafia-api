from bson import ObjectId
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, renderers
from api.models.area_model import *
from api.serializers import AreaSerializer
from api.library.utils import splitHeader
from api.models.role_model import Role


class AreaView(APIView):
    renderer_classes = [renderers.JSONRenderer]

    def get(self, request):
        if request.headers.get('Authorization') is None:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif request.headers.get('Authorization').find('Bearer') == -1:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        user = splitHeader(request.headers['Authorization'].split(' ')[1])
        if bool(user) is False:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        areas = Area.objects
        area_serializer = AreaSerializer(areas, many=True)
        return Response(area_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.headers.get('Authorization') is None:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif request.headers.get('Authorization').find('Bearer') == -1:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        user = splitHeader(request.headers['Authorization'].split(' ')[1])
        if bool(user) is False:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

        role = Role.objects(id=user.role_id).first()
        if role is None:
            return Response({'message': 'role not found'}, status=status.HTTP_400_BAD_REQUEST)

        if role.name in ['admin', 'manager']:
            area_serializer = AreaSerializer(data=request.data)
            if area_serializer.is_valid():
                area_serializer.save()
                return Response(area_serializer.data, status=status.HTTP_200_OK)
            return Response(area_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            print(role.name)
            return Response({"message": "only admin or manager have permission."}, status=status.HTTP_401_UNAUTHORIZED)


class AreaDetailView(APIView):
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

        area = Area.objects(id=id).first()
        area_serializer = AreaSerializer(area)
        return Response(area_serializer.data, status=status.HTTP_200_OK)

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

        area = Area.objects(id=id).first()
        area_serializer = AreaSerializer(area, data=request.data, partial=True)
        if area_serializer.is_valid():
            area.updated_at = datetime.datetime.utcnow()
            area_serializer.save()
        return Response(area_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        if request.headers.get('Authorization') is None:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif request.headers.get('Authorization').find('Bearer') == -1:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif not ObjectId.is_valid(id):
            return Response({'message': 'Object ID is not valid'}, status=status.HTTP_400_BAD_REQUEST)

        user = splitHeader(request.headers['Authorization'].split(' ')[1])
        if bool(user) is False:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

        area = Area.objects(id=id).first()
        area.delete()
        return Response({'message': 'deleted successfully.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def getAllArea(request: Request):
    if request.headers.get('Authorization') is None:
        return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
    elif request.headers.get('Authorization').find('Bearer') == -1:
        return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
    # elif not ObjectId.is_valid(area_id):
    #     return Response({'message': 'Object ID is not valid'}, status=status.HTTP_400_BAD_REQUEST)

    user = splitHeader(request.headers['Authorization'].split(' ')[1])
    if bool(user) is False:
        return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        offset = 0
        limit_record = 10
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
        print(offset, limit_record)
        list_area = Area.objects.skip(offset).limit(int(limit_record))
        list_area_serializer = AreaSerializer(list_area, many=True)
        return Response(list_area_serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': 'query page or limit record invalid'}, status=status.HTTP_400_BAD_REQUEST)