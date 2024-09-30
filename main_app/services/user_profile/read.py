from service_objects.services import Service
from models_app.models import UserProfile
from django.db.models import QuerySet
from django import forms

class ReadUserByID(Service):
    user_id = forms.IntegerField()

    def process(self) -> QuerySet:
        return UserProfile.objects.get(pk=self.cleaned_data['user_id'])
    
class ReadUserGithubPFP(Service):
    user_id = forms.IntegerField()

    def process(self) -> str:
        user =  UserProfile.objects.get(pk=self.cleaned_data['user_id'])
        social_profile = user.social_auth.first()
        if social_profile:
            github_id = social_profile.extra_data['id']
            return f'https://avatars.githubusercontent.com/u/{github_id}'
        else:
            return ''