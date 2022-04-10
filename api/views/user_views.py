import datetime
import json

from bson import ObjectId
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, renderers
from api.serializers import UserSerializer
from api.models.user_model import User
from api.models.role_model import Role
from api.library.utils import auth, encryption, generate_token, splitHeader
from collections import OrderedDict


def dynamically_user(user_serializer):
    try:
        role = Role.objects(id=ObjectId(user_serializer['role_id'])).first()
        user_serializer.pop('password', None)
        user_serializer['role_id'] = {
            'id': str(user_serializer['role_id']),
            'name': str(role.name)
        }
    except Exception as e:
        print(e)
    return user_serializer


class UserView(APIView):
    renderer_classes = [renderers.JSONRenderer]

    def get(self, request: Request):
        """
            List all user
            @param  self: class instance
            @param  request: received data from user's request
            @return Response: List of user and status
        """
        if request.headers.get('Authorization') is None:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif request.headers.get('Authorization').find('Bearer') == -1:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        user = splitHeader(request.headers['Authorization'].split(' ')[1])
        if bool(user) is False:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            list_user = User.objects
            user_role_login = Role.objects(id=user.role_id).first()

            if user_role_login.name == 'staff':
                return Response({'message': 'Forbidden.'}, status=status.HTTP_403_FORBIDDEN)

            print(user.username)
            if user_role_login.name == 'manager':
                list_user = User.objects(managed_by=str(user.id))

            serializers_users = UserSerializer(list_user, many=True)
            # update role information to user
            for user_serializer in serializers_users.data:
                dynamically_user(user_serializer)

            return Response(serializers_users.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request: Request):
        """
             Create a new user
             @param  self: class instance
             @param  request: received data from user's request
             @return Response: a user was created and status
        """
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

            if request.data.get('password') is not None:
                hashed_password = encryption(request.data['password'])
                request.data['password'] = encryption(request.data['password']).decode('utf-8')
            # request.data.update({'password': encryption(request.data['password'])})
            user_serializer = UserSerializer(data=request.data)

            if user_serializer.is_valid():  # check if data is validation
                saved_user = user_serializer.save()  # saved to db
                return Response(user_serializer.data, status=status.HTTP_200_OK)

            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'message': 'Bad request.'}.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    renderer_classes = [renderers.JSONRenderer]  # render format "application/json"

    def get(self, request: Request, id):
        """
             Get specified user with ObjectId
             @param  self: class instance
             @param  request: received data from user's request
             @param id: id of user
             @return Response: a specified user and status
        """

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
            user = User.objects(id=id).first()
            serializers_user = UserSerializer(user)
            # add role object to dict user
            result = dynamically_user(OrderedDict(serializers_user.data))

            if bool(user) is False:
                return Response({'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)

        return Response(result, status=status.HTTP_200_OK)

    def patch(self, request: Request, id):
        """
             Update specified fields of user
             @param  self: class instance
             @param  request: received data from user's request
             @param id: id of user
             @return Response: a updated user and status
        """
        if request.headers.get('Authorization') is None:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif request.headers.get('Authorization').find('Bearer') == -1:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif not ObjectId.is_valid(id):
            return Response({'message': 'Object ID is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        elif request.data.get('username') is not None:
            return Response({'message': 'cannot update username'}, status=status.HTTP_400_BAD_REQUEST)

        user_login = splitHeader(request.headers['Authorization'].split(' ')[1])
        if bool(user_login) is False:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

        print(user_login.username)
        try:
            user = User.objects(id=id).first()
            role_name_user_login = Role.objects(id=user_login['role_id']).first()['name']
            role_name_user = Role.objects(id=user['role_id']).first()['name']
            if role_name_user_login == 'staff' and user_login.username != user.username:
                return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
            elif (
                    role_name_user_login == 'manager' and user_login.username != user.username and role_name_user != 'staff'):
                return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

            if request.data.get('password') is not None:
                request.data['password'] = encryption(request.data['password']).decode('utf-8')

            if request.data.get('managed_by') is not None and role_name_user_login == 'staff':
                return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

            serializers_user = UserSerializer(user, data=request.data, partial=True)  # serializer data for validation

            if serializers_user.is_valid():
                user.updated_at = datetime.datetime.utcnow()  # update updated_at field
                serializers_user.save()  # save new instance to db
                result = dynamically_user(OrderedDict(serializers_user.data))

                return Response({
                    "message": "updated successfully.",
                    "data": result
                }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)

        return Response(serializers_user.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, id):
        """
             Delete  user
             @param  self: class instance
             @param  request: received data from user's request
             @param id: id of user
             @return Response: message and status
        """

        if request.headers.get('Authorization') is None:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif request.headers.get('Authorization').find('Bearer') == -1:
            return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif not ObjectId.is_valid(id):
            return Response({'message': 'Object ID is not valid'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_login = splitHeader(request.headers['Authorization'].split(' ')[1])
            if bool(user_login) is False:
                return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
            user_delete = User.objects(id=id).first()

            if bool(user_delete) is False:
                return Response({'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

            role_user_login = Role.objects(id=user_login.role_id).first()['name']
            role_user_delete = Role.objects(id=user_delete.role_id).first()['name']

            print(role_user_login, role_user_delete)

            role_admin = Role.objects(name='admin').first()

            if (role_user_login == 'admin' and role_user_delete != 'admin') or (
                    role_user_login == 'manager' and role_user_delete == 'staff') and user_login.username != user_delete.username:
                if role_user_delete == 'manager':
                    user_admin = User.objects(role_id=str(role_admin.id)).first()
                    staff_managed_by_user = User.objects(managed_by=str(user_delete.id))
                    for staff_user in staff_managed_by_user:
                        staff_user.managed_by = str(user_admin.id)
                        print(staff_user.managed_by)
                        staff_user.save()
                        print('flag')

                user_delete.delete()
                print('da xoa')
            else:
                return Response({'message': 'Authorization invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
        return Response({'message': 'deleted successfully'}, status=status.HTTP_200_OK)


class LoginView(APIView):
    def post(self, request: Request):
        """
             Login to access api interface
             @param  self: class instance
             @param  request: received data from user's request
             @return Response: user and status
        """
        try:
            json_data = json.loads(request.body)
            username, password = json_data['username'], json_data['password']

            user = auth(username, password)
            role_name = Role.objects(id=user.role_id).first()['name']
            token = generate_token(username, password, role_name)
        except Exception as e:
            print(e)
            return Response({'message': 'Authentication invalid.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            serializers_user = UserSerializer(user)
            if bool(user) is False:
                return Response({'message': 'Username or password invalid.'}, status=status.HTTP_400_BAD_REQUEST)
            # add role to dict user
            result = dynamically_user(OrderedDict(serializers_user.data))
        except Exception as e:
            print(e)

        return Response({
            'data': result,
            'token': token
        }, status=status.HTTP_200_OK)
