from urllib.parse import parse_qs
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from channels.auth import AuthMiddlewareStack
from rest_framework_simplejwt.tokens import AccessToken


User = get_user_model()


class TokenMiddleware:
    """
    Token middleware
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        close_old_connections()
        query_strings = parse_qs(scope['query_string'].decode())
        token = query_strings.get('token')
        if not token:
            scope['user'] = AnonymousUser()
            return self.inner(scope)
        try:
            access_token = AccessToken(token[0])
            user = User.objects.get(id=access_token['id'])
        except Exception as exception:
            scope['user'] = AnonymousUser()
            return self.inner(scope)
        if not user.is_active:
            scope['user'] = AnonymousUser()
            return self.inner(scope)
        scope['user'] = user
        return self.inner(scope)


def TokenAuthMiddlewareStack(inner):
    """
    Our new middleware class plucks the JWT access token from the query string and retrieves the associated user. Once
    the WebSocket connection is opened, all messages can be sent and received without verifying the user again. Closing
    the connection and opening it again requires re-authorization.
    :param inner:
    :return:
    """
    return TokenMiddleware(AuthMiddlewareStack(inner))
