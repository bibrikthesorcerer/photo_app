from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from service_objects.errors import ValidationError
from django import forms
from django.db.models import Q
from django.db.utils import IntegrityError

from models_app.models import Like, UserProfile, Photo


class UpdateOrCreateLike(ServiceWithResult):
    user = ModelField(UserProfile)
    photo_id = forms.IntegerField()

    custom_validations = ["_photo_exists"]

    def process(self):
        self.run_custom_validations()
        self.result = self._create_or_update_like()
        return self

    def _photo_exists(self):
        photo_id = self.cleaned_data.get("photo_id")
        try:
            self.photo = Photo.objects.get(id=photo_id)
        except Photo.DoesNotExist:
            self.add_error("photo_id", ValidationError(message="Photo with given id not found"))
            self.stop_process()

    def _create_or_update_like(self):
        user = self.cleaned_data.get("user")
        like_obj, _created = Like.objects.update_or_create(
            photo=self.photo,
            user=user,
            defaults={"deleted_at": None},
        )
        return like_obj
