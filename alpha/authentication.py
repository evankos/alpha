import functools

import pytz
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
import datetime


from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


from channels.handler import AsgiRequest
from rest_framework.settings import api_settings
authenticators = [auth() for auth in api_settings.DEFAULT_AUTHENTICATION_CLASSES]


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted')

        # This is required for the time comparison
        utc_now = datetime.utcnow()
        utc_now = utc_now.replace(tzinfo=pytz.utc)

        if token.created < utc_now - datetime.timedelta(hours=24):
            raise AuthenticationFailed('Token has expired')

        return token.user, token





class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        if not created:
            # update the created time of the token to keep it valid
            token.created = datetime.datetime.utcnow()
            token.save()
        return Response({'token': token.key})




def rest_auth(func):
    """
    Wraps a HTTP or WebSocket connect consumer (or any consumer of messages
    that provides a "cookies" or "get" attribute) to provide a "http_session"
    attribute that behaves like request.session; that is, it's hung off of
    a per-user session key that is saved in a cookie or passed as the
    "session_key" GET parameter.
    It won't automatically create and set a session cookie for users who
    don't have one - that's what SessionMiddleware is for, this is a simpler
    read-only version for more low-level code.
    If a message does not have a session we can inflate, the "session" attribute
    will be None, rather than an empty session you can write to.
    Does not allow a new session to be set; that must be done via a view. This
    is only an accessor for any existing session.
    """
    @functools.wraps(func)
    def inner(message, *args, **kwargs):
        # Make sure there's NOT a http_session already
        try:
            # We want to parse the WebSocket (or similar HTTP-lite) message
            # to get cookies and GET, but we need to add in a few things that
            # might not have been there.
            if "method" not in message.content:
                message.content['method'] = "FAKE"
            request = AsgiRequest(message)

        except Exception as e:
            raise ValueError("Cannot parse HTTP message - are you sure this is a HTTP consumer? %s" % e)
        # Make sure there's a session key
        user = None
        auth = None
        auth_token = request.GET.get("token", None)

        if auth_token:
            # comptatibility with rest framework
            request._request = {}
            request.META["HTTP_AUTHORIZATION"] = "Token %s" % auth_token
            for authenticator in authenticators:
                try:
                    user_auth_tuple = authenticator.authenticate(request)
                except AuthenticationFailed:
                    pass

                if user_auth_tuple is not None:
                    message._authenticator = authenticator
                    user, auth = user_auth_tuple
                    break
        message.user, message.auth = user, auth
        # Make sure there's a session key
        # Run the consumer
        result = func(message, *args, **kwargs)
        return result
    return inner







obtain_auth_token = ObtainAuthToken.as_view()