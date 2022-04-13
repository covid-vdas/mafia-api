from rest_framework import serializers
from api.models import *
from api.models.camera_model import *
from rest_framework_mongoengine import serializers as serializer_mongoengine


class ImageSerializer(serializer_mongoengine.DocumentSerializer):
    class Meta:
        model = Image
        fields = '__all__'

#
# class VideoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Video
#         fields = '__all__'
#

# class CameraSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Camera
#         fields = '__all__'


class UserSerializer(serializer_mongoengine.DocumentSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RoleSerializer(serializer_mongoengine.DocumentSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class CameraSerializer(serializer_mongoengine.DocumentSerializer):
    class Meta:
        model = Camera
        fields = '__all__'


class AreaSerializer(serializer_mongoengine.DocumentSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class ViolationSerializer(serializer_mongoengine.DocumentSerializer):
    class Meta:
        model = Violation
        fields = '__all__'


class ViolationTypeSerializer(serializer_mongoengine.DocumentSerializer):
    class Meta:
        model = ViolationType
        fields = '__all__'


class ObjectClassSerializer(serializer_mongoengine.DocumentSerializer):
    class Meta:
        model = ObjectInformation
        fields = '__all__'
