from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.compat import set_rollback
from rest_framework import exceptions, status
from . import log_service
from django.contrib.auth.models import User

def generic_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.

    if context is not None:
        user = context['request'].user
        if isinstance(user, User): log_service.log(str(exc),user)


    headers = {}
    if getattr(exc, 'auth_header', None):
        headers['WWW-Authenticate'] = exc.auth_header
    if getattr(exc, 'wait', None):
        headers['Retry-After'] = '%d' % exc.wait

    if isinstance(exc, exceptions.APIException):


        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {'detail': exc.detail}

        set_rollback()
        response = Response(data, status=exc.status_code, headers=headers)
    elif isinstance(exc, Exception): #TODO more fine grained exception handling

        data = {'detail': str(exc)}
        set_rollback()
        response = Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR, headers=headers)


    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response
