from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from django import forms
from django.db.models import QuerySet

from models_app.models.like.models import Like
from models_app.models.photo.models import Photo
from models_app.models.user_profile.models import UserProfile

class UpdateOrCreateLike(ServiceWithResult):
    photo = ModelField(Photo)
    user = ModelField(UserProfile)

    def process(self) -> QuerySet:
        photo = self.cleaned_data['photo']
        user = self.cleaned_data['user']
        self.result, _ = Like.objects.update_or_create(
            photo=photo,
            user=user,
            defaults={"deleted_at": None},
            create_defaults={"photo": photo, "user": user}
        )
        return self.result