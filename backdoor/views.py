from django.db.transaction import atomic
from django.http import JsonResponse, QueryDict
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User,Group
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import viewsets, status, authentication, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
import ast
from backdoor.utils.validator import validated
from .serializers import GroupSerializer, PostSerializer, UserSerializer
from django.core.serializers import serialize
from backdoor.models import Post, Location
import json
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D


class Users(APIView):

    def get(self, request, format=None):
        """
        API endpoint that allows users to be viewed.
        """
        users = User.objects.all().order_by('-date_joined')
        serialized = UserSerializer(users, many=True)
        return JsonResponse(serialized.data, safe=False)

    @atomic
    @validated(UserSerializer)
    def post(self, request, format=None):
        user = request.validated_object
        user.save()
        return Response(status=status.HTTP_200_OK)

    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (permissions.AllowAny() if self.request.method == 'POST'
                else IsAdminUser()),


class Groups(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        """
        API endpoint that allows users to be viewed or edited.
        """
        groups = Group.objects.all()
        serialized = GroupSerializer(groups, many=True)
        return JsonResponse(serialized.data, safe=False)


class Posts(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        latlon=request.query_params
        pnt = GEOSGeometry('SRID=28992;POINT(%s %s)'%(latlon['lat'],latlon['lon']))
        meters = float(latlon['range'])
        posts = Post.objects.filter(point__distance_lte=(pnt, meters * 1e-05))
        serialized = PostSerializer(posts, many=True)
        return JsonResponse(serialized.data, safe=False)

    @atomic
    @validated(PostSerializer)
    def post(self, request, format=None):

        post = request.validated_object
        post.user = request.user
        post.save()
        refresh_user_location(request)
        return Response(status=status.HTTP_200_OK)




def refresh_user_location(request):
    try:
        location = request.user.location
        location.point = request.validated_object.point
        location.save()
    except Exception as e:#TODO more specific exception handling
        location = Location(user_account=request.user, point=request.validated_object.point)
        location.save()


# create_user = CreateUser.as_view()
posts = Posts.as_view()
groups = Groups.as_view()
users = Users.as_view()


