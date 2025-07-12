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