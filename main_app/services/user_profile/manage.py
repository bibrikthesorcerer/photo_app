from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from django import forms
    
from models_app.models import UserProfile
from models_app.admin.user_profile.forms import UserProfileForm


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