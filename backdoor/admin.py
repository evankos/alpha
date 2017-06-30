from django.contrib import admin
from backdoor.models import Exception, Post
# Register your models here.

@admin.register(Exception, Post)
class UserAdmin(admin.ModelAdmin):
    pass