from django import forms
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from rest_framework_simplejwt.tokens import AccessToken
from datetime import datetime, timedelta
from decouple import config

from models_app.models import UserProfile
from api.utils import retrieve_value, delete_value, cache_value


class SetNewUserApiToken(ServiceWithResult):
    user = ModelField(UserProfile)
    lifetime = forms.IntegerField(required=False)

    def process(self):
        self.user = self.cleaned_data.get("user")
        self._delete_old_token()
        self.result = self._generate_new_token()
        return self
    
    def _delete_old_token(self):
        old_token_str = retrieve_value(f'access_tokens:{self.user.username}')
        if old_token_str is not None:
            delete_value(f'access_tokens:{self.user.username}')

    def _generate_new_token(self) -> AccessToken:
        new_token = AccessToken().for_user(self.user)
        lifetime = self.cleaned_data.get('lifetime')
        if lifetime:
            new_token.set_exp(
                from_time=new_token.current_time,
                lifetime=timedelta(seconds=lifetime)
            )
        new_token.created = datetime.fromtimestamp(new_token['iat']).strftime('%Y-%m-%d %H:%M:%S')
        redis_ttl = lifetime or config("ACCESS_TOKEN_LIFETIME")
        cache_value(f'access_tokens:{self.user.username}', str(new_token), redis_ttl)
        return new_token