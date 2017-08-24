from django.conf.urls import url,include
from rest_framework import routers
from . import views
from rest_framework.authtoken.views import obtain_auth_token

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)



urlpatterns = [
    url(r'^users/', views.users),
    url(r'^groups/', views.groups),
    url(r'^posts/',views.posts),
    url(r'^auth/', obtain_auth_token)
]



