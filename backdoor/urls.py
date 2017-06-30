from django.conf.urls import url,include
from rest_framework import routers
from . import views

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)



urlpatterns = [
    url(r'^users/',views.ListUsers),
    url(r'^groups/',views.ListGroups),
    url(r'^posts/',views.Posts),
]
