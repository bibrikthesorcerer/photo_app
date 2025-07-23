from django import forms
from service_objects.services import ServiceWithResult, ServiceOutcome
from service_objects.fields import ModelField
from service_objects.errors import ValidationError, AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from datetime import datetime, timedelta, timezone
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
        old_token_str = retrieve_value(f'access_tokens:{self.user.id}')
        if old_token_str is not None:
            delete_value(f'access_tokens:{self.user.id}')

    def _generate_new_token(self) -> AccessToken:
        new_token = AccessToken().for_user(self.user)
        lifetime = self.cleaned_data.get('lifetime')
        if lifetime:
            new_token.set_exp(
                from_time=new_token.current_time,
                lifetime=timedelta(seconds=lifetime)
            )
        new_token.payload["created"] = datetime.now(timezone.utc).timestamp()
        redis_ttl = lifetime or config("ACCESS_TOKEN_LIFETIME")
        cache_value(f'access_tokens:{self.user.id}', str(new_token), redis_ttl)
        return new_token
    

class AuthenticateUserAndRenewApiToken(ServiceWithResult):
    email = forms.EmailField()
    password = forms.CharField()

    custom_validations = ["_get_user_profile", "_check_password"]

    def process(self):
        self.run_custom_validations()
        self.result = self._renew_token()
        return self
    
    def _get_user_profile(self):
        email = self.cleaned_data.get('email')
        try:
            self.user = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            self.add_error("email", ValidationError(message="User with given email doesn't exist"))
            self.stop_process()

    def _check_password(self):
        if not self.user.check_password(self.cleaned_data.get("password")):
            self.add_error("password", AuthenticationFailed(message="Given password is not correct"))
            self.stop_process()

    def _renew_token(self) -> AccessToken:
        return ServiceOutcome(
            SetNewUserApiToken,
            {"user": self.user}
        ).result


class DeleteUserApiToken(ServiceWithResult):
    user = ModelField(UserProfile)

    def process(self):
        self.user = self.cleaned_data.get("user")
        self._renew_valid_token_ts()
        self._delete_token()
        return self
    
    def _delete_token(self):
        token_str = retrieve_value(f'access_tokens:{self.user.id}')
        if token_str is not None:
            delete_value(f'access_tokens:{self.user.id}')

    def _renew_valid_token_ts(self):
        cache_value(f'access_tokens:rot_timestamp:{self.user.id}', datetime.now(timezone.utc).timestamp())