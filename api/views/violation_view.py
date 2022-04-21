import datetime
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
from collections import OrderedDict
from api.models.violation_type_model import *
from api.models.object_information import *
from api.models.image_model import *
from django.http import JsonResponse


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
            result_violation = dynamically_camera(OrderedDict(camera_serializer.data))
            return Response(result_violation, status=status.HTTP_200_OK)
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

        total_count = Violation.objects(camera_id=camera_id).count()
        list_violation_by_camera = Violation.objects(camera_id=camera_id).aggregate(
            [
                {
                    '$addFields': {
                        'camera_object_id': {'$toObjectId': '$camera_id'}
                    }
                },
                {
                    '$lookup': {
                        'from': 'violation_type',
                        'localField': 'type_id',
                        'foreignField': '_id',
                        'as': 'violation_type_arr'
                    }
                },
                {
                    '$unwind': '$violation_type_arr'
                },
                {
                    '$lookup': {
                        'from': 'object_information',
                        'localField': 'class_id',
                        'foreignField': '_id',
                        'as': 'information_arr'
                    }
                },
                {
                    '$unwind': '$information_arr'
                },
                {
                    '$lookup': {
                        'from': 'image',
                        'localField': 'image_id',
                        'foreignField': '_id',
                        'as': 'image_arr'
                    }
                },
                {
                    '$unwind': '$image_arr'
                },
                {
                    '$lookup': {
                        'from': 'camera',
                        'localField': 'camera_object_id',
                        'foreignField': '_id',
                        'as': 'camera_arr'
                    }
                },
                {
                    '$unwind': '$camera_arr'
                },
                {
                    '$sort': {
                        'created_at': 1
                    }
                }
            ]
        )
        custom_violation_arr = []
        for violation in list_violation_by_camera:
            custom_violation = {
                'type_id': {
                    'id': str(violation['violation_type_arr']['_id']),
                    'name': violation['violation_type_arr']['name']
                },
                'camera_id': {
                    'id': str(violation['camera_arr']['_id']),
                    'name': violation['camera_arr']['name']
                },
                'class_id': {
                    'id': str(violation['violation_type_arr']['_id']),
                    'name': violation['information_arr']['name']
                },
                'image_id': {
                    'id': str(violation['violation_type_arr']['_id']),
                    'name': violation['image_arr']['name']
                },
                'distance': float(violation.get('distance', 1)),
                'created_at': violation['created_at'],
                'updated_at': violation['updated_at']
            }
            custom_violation_arr.append(custom_violation)
            # dynamically_camera(violation)
        print(violation)
        # list_violation_by_camera_serializer = ViolationSerializer(list_violation_by_camera, many=True)
        return JsonResponse({
            'total': total_count,
            'data': list(custom_violation_arr)
        }, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'message': 'query page or limit record invalid'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)


# @api_view(['GET'])
# def listViolationByCamera(request: Request, camera_id):
#
#     if request.headers.get('Authorization') is None:
#         return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
#     elif request.headers.get('Authorization').find('Bearer') == -1:
#         return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
#     elif not ObjectId.is_valid(camera_id):
#         return Response({'message': 'Object ID is not valid'}, status=status.HTTP_400_BAD_REQUEST)
#
#     user = splitHeader(request.headers['Authorization'].split(' ')[1])
#     if bool(user) is False:
#         return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
#     try:
#         offset = 0
#         limit_record = 0
#         page_number = 1
#
#         if bool(request.query_params.get('limit')) is True:
#             limit_record = request.query_params.get('limit')
#             if not limit_record.isdigit():
#                 return Response({'message': 'limit record invalid'}, status=status.HTTP_400_BAD_REQUEST)
#
#         if bool(request.query_params.get('page')) is True:
#             page_number = request.query_params.get('page')
#             if page_number.isdigit():
#                 offset = (int(page_number) - 1) * int(limit_record)
#             else:
#                 return Response({'message': 'query page invalid'}, status=status.HTTP_400_BAD_REQUEST)
#         to_date = datetime.datetime.now()
#         report_time = 7
#         if request.query_params.get('from-date') is not None:
#             report_time = int(request.query_params.get('from-date'))
#         from_date = to_date - datetime.timedelta(days=report_time) #datetime.datetime.strptime(from_date_str, '%Y-%m-%d').date()   #.timedelta(days=3)
#
#         list_from_to_date = Violation.objects(camera_id=camera_id).filter(created_at__gte=from_date, created_at__lt=to_date).aggregate(
#             [
#                 {
#                     '$group': {
#                         '_id': {
#                             'camera_id': '$camera_id',
#                             'created_at': {
#                                 '$dateToString': {
#                                     'format': '%Y-%m-%d',
#                                     'date': '$created_at'
#                                 }
#                             },
#                         },
#                         'count': {'$sum': 1}
#                     }
#                 }
#             ]
#         )
#         print(list(list_from_to_date))
#         total_case_each_day = []
#         total_distance = 0
#         total_facemask = 0
#         total_violation_custom_day = 0
#         for case_day in list_from_to_date:
#             case_each_day = {
#                 'faceMask': 0,
#                 'distance': 0
#             }
#             day_created_at_to_date = datetime.datetime.strptime(case_day['_id']['created_at'], '%Y-%m-%d').strftime('%Y-%m-%dT%H:%M:%S.%f')
#             from_date = datetime.datetime.fromisoformat(day_created_at_to_date)
#             to_date = from_date.replace(hour=0, minute=0, second=0) + datetime.timedelta(days=1)
#             list_violation = Violation.objects(camera_id=case_day['_id']['camera_id']).filter(created_at__lt=to_date, created_at__gt=from_date)
#             for violation in list_violation:
#                 violation_type = ViolationType.objects.get(id=ObjectId(violation.type_id))
#                 if violation_type.name == 'Facemask':
#                     total_facemask += 1
#                     case_each_day['faceMask'] += 1
#                 else:
#                     total_distance += 1
#                     case_each_day['distance'] += 1
#                 total_violation_custom_day += 1
#             case_each_day['date'] = violation.created_at.strftime('%Y-%m-%d')
#             total_case_each_day.append(case_each_day)
#         return Response({
#             'total_violation_customDays': total_violation_custom_day,
#             'total_distance': total_distance,
#             'total_facemask': total_facemask,
#             'total_customDays': total_case_each_day,
#         }, status=status.HTTP_200_OK)
#     except Exception as e:
#         print(e)
#         return Response({'message': 'query page or limit record invalid'}, status=status.HTTP_400_BAD_REQUEST)
#     return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def listViolationByCamera(request: Request, camera_id):
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
        to_date = datetime.datetime.now()
        report_time = 7
        if request.query_params.get('from-date') is not None:
            report_time = int(request.query_params.get('from-date'))
        from_date = to_date - datetime.timedelta(
            days=report_time)  # datetime.datetime.strptime(from_date_str, '%Y-%m-%d').date()   #.timedelta(days=3)

        list_from_to_date = Violation.objects(camera_id=camera_id).filter(created_at__gte=from_date,
                                                                          created_at__lt=to_date).aggregate(
            [
                {
                    '$group': {
                        '_id': {
                            'camera_id': '$camera_id',
                            'created_at': {
                                '$dateToString': {
                                    'format': '%Y-%m-%d',
                                    'date': '$created_at'
                                }
                            },
                        },
                        'count': {'$sum': 1},
                        'total_distance': {
                            '$sum': {'$cond': [{'$eq': ['$type_id', ObjectId('62176a1e904ecd9fa640fb62')]}, 1, 0]}
                        },
                        'total_mask': {
                            '$sum': {'$cond': [{'$eq': ['$type_id', ObjectId('621767af45207bf3596650a0')]}, 1, 0]}
                        }
                    }
                },
                {
                    '$sort': {
                        '_id.created_at': 1
                    }
                }
            ]
        )

        total_violation_all_days = 0
        total_distance = 0
        total_facemask = 0
        list_total_violation = []
        for violation in list_from_to_date:
            total_facemask += int(violation['total_mask'])
            total_distance += int(violation['total_distance'])

            list_total_violation.append({
                'day': violation['_id']['created_at'],
                'facemask': violation['total_mask'],
                'distance': violation['total_distance']
            })
            total_violation_all_days += violation['count']

        return Response({
            'total_violation': total_violation_all_days,
            'total_distance': total_distance,
            'total_facemask': total_facemask,
            'data': list_total_violation
        }, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'message': 'query page or limit record invalid'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)


def dynamically_camera(violation_serializer):
    """
        @ user_serializer: OrderedList

        transforms role_id to store id and name

        return OrderedList
    """
    try:
        camera = Camera.objects.get(id=ObjectId(violation_serializer['camera_id']))
        violation_type = ViolationType.objects.get(id=violation_serializer['type_id'])
        object_information = ObjectInformation.objects.get(id=violation_serializer['class_id'])
        image = Image.objects.get(id=violation_serializer['image_id'])

        violation_serializer.update({
            'type_id': {
                'id': str(violation_serializer['type_id']),
                'name': str(violation_type.name)
            },
            'camera_id': {
                'id': str(violation_serializer['camera_id']),
                'name': str(camera.name)
            },
            'class_id': {
                'id': str(violation_serializer['type_id']),
                'name': str(object_information.name)
            },
            'image_id': {
                'id': str(violation_serializer['image_id']),
                'name': str(image.name)
            }
        })

    except Exception as e:
        print(e)
    return violation_serializer
