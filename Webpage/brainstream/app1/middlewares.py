from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()

class UsernameWebsocketMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return UsernameWebsocketMiddlewareInstance(scope, self)

class UsernameWebsocketMiddlewareInstance:
    def __init__(self, scope, middleware):
        self.scope = scope
        self.inner = middleware.inner

    def __call__(self, receive, send):
        self.scope['user'] = self.get_user()
        return self.inner(self.scope)(receive, send)

    def get_user(self):
        query_string = parse_qs(self.scope['query_string'].decode())
        token = query_string.get('token')
        if not token:
            return AnonymousUser()
        try:
            access_token = AccessToken(token[0])
            user = User.objects.get(id=access_token['id'])
        except Exception:
            return AnonymousUser()
        if not user.is_active:
            return AnonymousUser()
        return user
