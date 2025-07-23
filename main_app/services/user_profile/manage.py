from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from django import forms
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth.forms import SetPasswordForm
    
from models_app.models import UserProfile
from models_app.admin.user_profile.forms import UserProfileForm
from main_app.tokens import account_oauth_link_token_generator
from decouple import config
from rest_framework_simplejwt.tokens import AccessToken
from datetime import datetime, timedelta, timezone

from main_app.utils.redis import cache_value, retrieve_value, delete_value


class GetUserGithubPFP(ServiceWithResult):
    user = ModelField(UserProfile)

    def process(self) -> str:
        user =  self.cleaned_data.get('user')
        social_profile = user.social_auth.first()
        self.result = ''
        if social_profile:
            github_id = social_profile.extra_data['id']
            self.result = f'https://avatars.githubusercontent.com/u/{github_id}'
        
        return self.result
    
class UpdateUserProfile(ServiceWithResult):
    user = ModelField(UserProfile)
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)

    def _collect_form_data(self) -> dict[str, str]:
        return {"username": self.cleaned_data.get("username"),
                "email": self.cleaned_data.get("email"),
                "first_name": self.cleaned_data.get("first_name"),
                "last_name": self.cleaned_data.get("last_name")}
    
    def process(self) -> bool:
        user = self.cleaned_data.get('user')
        form = UserProfileForm(self._collect_form_data(), instance=user)
        self.result = False
        if form.is_valid():
            form.save()
            self.result = True
        return self.result
    

class FormAccountLinkEmail(ServiceWithResult):
    user = ModelField(UserProfile)
    domain = forms.CharField()
    protocol = forms.CharField()

    def process(self):
        self.result = self._form_verification_email()
        return self
    
    def _form_verification_email(self):
        user = self.cleaned_data.get("user")
        token = account_oauth_link_token_generator.make_token(user)
        user_idb64 = urlsafe_base64_encode(force_bytes(user.pk))
        opts = {"token": token, "user_idb64": user_idb64} | self.cleaned_data
        return render_to_string('registration/link_oauth_email.html', opts)


class SetPasswordForUser(ServiceWithResult):
    user = ModelField(UserProfile)
    new_password1 = forms.CharField()
    new_password2 = forms.CharField()

    def process(self):
        form = SetPasswordForm(user=self.cleaned_data.get("user"), data=self.cleaned_data)
        user = None
        if form.is_valid():
            user = form.save()
        self.result = (user, form)
        return self

class GetUserAPIToken(ServiceWithResult):
    user = ModelField(UserProfile)

    def process(self):
        user = self.cleaned_data.get('user')
        token_str = retrieve_value(f'access_tokens:{user.id}')
        try:
            self.result = AccessToken(token_str)
            self.result.created = datetime.fromtimestamp(self.result['iat']).strftime('%Y-%m-%d %H:%M:%S')
            return self.result
        except Exception: # expired token
            return None
    
class IssueNewUserAPIToken(ServiceWithResult):
    user = ModelField(UserProfile)
    lifetime = forms.IntegerField(required=False)

    def _clean_old_token(self, user):
        token = GetUserAPIToken.execute({"user":user})
        if token is not None:
            delete_value(f'access_tokens:{user.id}')

    def _generate_new_token(self, user):
        new_token = AccessToken().for_user(user)
        lifetime = self.cleaned_data.get('lifetime')
        if lifetime:
            new_token.set_exp(
                from_time=new_token.current_time,
                lifetime=timedelta(seconds=lifetime)
            )
        new_token.payload["created"] = datetime.now(timezone.utc).timestamp()
        redis_ttl = self.cleaned_data.get("lifetime") or config("ACCESS_TOKEN_LIFETIME")
        cache_value(f'access_tokens:{user.id}', str(new_token), redis_ttl)
        return new_token

    def process(self):
        user = self.cleaned_data.get('user')
        self._clean_old_token(user)
        self.result = self._generate_new_token(user)
        return self.result
