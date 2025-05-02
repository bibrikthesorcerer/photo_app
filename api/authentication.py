from rest_framework import authentication
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import AccessToken

from models_app.models import UserProfile

class RedisJWTAuth(authentication.BaseAuthentication):

    def _get_user_instance(self, uid):
        try:
            return UserProfile.objects.get(id=uid)
        except UserProfile.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        
    def _parse_header(self, request):
        header = request.META.get('HTTP_AUTHORIZATION')
        if not header:
            return None
        
        header_parts = header.split()
        if len(header_parts) == 0:
            # Empty AUTHORIZATION header sent
            raise exceptions.AuthenticationFailed(
                "Credentials were not provided"
            )

        if header_parts[0] != "Bearer":
            # Assume the header does not contain a JSON web token
            raise exceptions.AuthenticationFailed(
                "Expected JWT is Authorization header"
            )

        if len(header_parts) != 2:
            raise exceptions.AuthenticationFailed(
                "Authorization header must contain two space-delimited values"
            )

        return header_parts[1]
    
    def _retrieve_provided_token(self, raw_token):
        try:
            return AccessToken(raw_token)
        except Exception as e:
            raise exceptions.AuthenticationFailed(
                f"Invalid token provided: {e.args[0]}"
            )

    def authenticate(self, request):
        raw_token = self._parse_header(request)
        if raw_token is None:
            return None
        provided_token = self._retrieve_provided_token(raw_token)
        user = self._get_user_instance(provided_token['user_id'])
        return (user, None)