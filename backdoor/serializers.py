
from rest_framework import serializers
from .utils.geo_serializer import PointField


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)


class GroupSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)


class PostSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1000, min_length=5)
    point = PointField(max_length=10)






