from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser, AbstractBaseUser
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError

from api.authentication import RedisJWTAuth


class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, recieve, send):
        query_string = scope.get("query_string", b"").decode() # stored as byte-string https://github.com/django/asgiref/blob/main/specs/www.rst#http-connection-scope
        params = parse_qs(query_string)
        tokens = params.get("token")
        if tokens:
            user: AbstractBaseUser = await self.get_user_from_jwt(tokens[0])
            print(user)
            if user and not user.is_anonymous:
                scope["user"] = user
        
        return await self.inner(scope, recieve, send)

    @database_sync_to_async
    def get_user_from_jwt(self, token):
        try:
            auth = RedisJWTAuth()
            parsed_token = auth._retrieve_provided_token(token)
            return auth._get_user_instance(parsed_token['user_id'])
        except (AuthenticationFailed, TokenError) as e:
            return AnonymousUser()