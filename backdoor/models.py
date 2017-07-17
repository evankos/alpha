# from django.db import models
from django.contrib.gis.db import models
# Create your models here.

from django.contrib.auth.models import User


class Exception(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    occurence_date = models.DateTimeField("date occured")

    def __str__(self):
        return self.message


class Location(models.Model):
    user_account = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    point = models.PointField(srid=28992)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    point = models.PointField(srid=28992)