from service_objects.services import Service
from service_objects.fields import ModelField
from django import forms
from django.db.models import QuerySet

from models_app.models.like.models import Like
from models_app.models.photo.models import Photo
from models_app.models.user_profile.models import UserProfile

class GetOrCreateLike(Service):
    photo = ModelField(Photo)
    user = ModelField(UserProfile)

    def process(self) -> QuerySet:
        photo = self.cleaned_data['photo']
        user = self.cleaned_data['user']
        return Like.objects.get_or_create(photo=photo, user=user)