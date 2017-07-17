from django.contrib.auth.models import User, Group
from rest_framework import serializers

from backdoor.models import Post
from .utils.geo_serializer import PointField
from django.contrib.gis.db.models import PointField as PointFieldKey

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'username', 'email',)
        extra_kwargs = {
            'password': {'write_only': True}
        }
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined',)

    def post_validation(self):
        pass

    def save(self, validated_data):
        user = User(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        return user



class GroupSerializer(serializers.Serializer):
    class Meta:
        model = Group
        fields = ('name',)

    def post_validation(self):
        pass


class PostSerializer(serializers.ModelSerializer):

    def __init__(self,*args,**kwargs):
        super(PostSerializer, self).serializer_field_mapping[PointFieldKey] = PointField
        super(PostSerializer, self).__init__(*args,**kwargs)

    class Meta:
        model = Post
        fields = ('message', 'point',)

    def post_validation(self):
        pass

    def save(self, validated_data):
        return Post(message=validated_data['message'],
                    point=validated_data['point'])
    # message = serializers.CharField(max_length=1000, min_length=5)
    # point = PointField(max_length=10)





