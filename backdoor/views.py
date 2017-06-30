from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User,Group
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, GroupSerializer, PostSerializer
from django.core.serializers import serialize
from backdoor.models import Post, Location
import json
from django.contrib.gis.geos import Point

@api_view(['GET'])
@permission_classes((IsAdminUser,))
def ListUsers(request):
    """
    API endpoint that allows users to be viewed or edited.
    """
    users = User.objects.all().order_by('-date_joined')
    serialized = UserSerializer(users, many=True)
    return JsonResponse(serialized.data, safe=False)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
# @throttle_classes([OncePerDayUserThrottle])
def ListGroups(request):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    groups = Group.objects.all()
    serialized = GroupSerializer(groups, many=True)
    return JsonResponse(serialized.data, safe=False)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def Posts(request):

    if request.method == 'POST':
        post = Post(user=request.user,message=request.data['message'],
                    point=Point(request.data['point']))
        post.save()
        refresh_user_location(request)
        return Response()
    elif request.method == 'GET':
        posts = Post.objects.all()
        serialized = PostSerializer(posts, many=True)
        return JsonResponse(serialized.data, safe=False)

def refresh_user_location(request):
    try:
        user_location = Location.objects.get(user_account=request.user)
    except:
        Location(user_account=request.user, point=Point()).save()