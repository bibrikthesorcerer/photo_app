from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from django import forms
    
from models_app.models import UserProfile


class GetUserGithubPFP(ServiceWithResult):
    user = ModelField(UserProfile)

    def process(self) -> str:
        user =  self.cleaned_data['user']
        social_profile = user.social_auth.first()
        self.result = ''
        if social_profile:
            github_id = social_profile.extra_data['id']
            self.result = f'https://avatars.githubusercontent.com/u/{github_id}'
        
        return self.result