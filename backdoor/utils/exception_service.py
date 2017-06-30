from rest_framework.views import exception_handler
from . import log_service

from django.contrib.auth.models import User

def generic_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.

    if context is not None:
        user = context['request'].user
        if isinstance(user, User): log_service.log(str(exc),user)

    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response
