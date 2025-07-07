from service_objects.services import ServiceWithResult, ServiceOutcome
from service_objects.fields import ModelField
from service_objects.errors import ValidationError, ServiceObjectLogicError
from django import forms
from django.db.models import Q
from django.db.utils import IntegrityError

from models_app.models import Like, UserProfile, Photo
from notifications.utils.senders import send_message_to_list_of_users
from api.services import RetrievePhoto


class UpdateOrCreateLike(ServiceWithResult):
    user = ModelField(UserProfile)
    photo_id = forms.IntegerField()

    custom_validations = ["_photo_exists"]

    def process(self):
        self.run_custom_validations()
        self.result = self._create_or_update_like()
        self._send_notification_for_photo_author()
        return self

    def _photo_exists(self):
        try:
            self.photo = ServiceOutcome(
                RetrievePhoto,
                self.cleaned_data
            ).result
        except ServiceObjectLogicError: #Photo.DoesNotExist:
            self.add_error("photo_id", ValidationError(message="Photo with given id not found"))
            self.stop_process()

    def _create_or_update_like(self):
        self.user = self.cleaned_data.get("user")
        like_obj, _created = Like.objects.update_or_create(
            photo=self.photo,
            user=self.user,
            defaults={"deleted_at": None},
        )
        return like_obj
    
    def _send_notification_for_photo_author(self):
        if self.photo.user != self.user:
            send_message_to_list_of_users(
                [self.photo.user.id],
                "notify_like",
                f"User {self.user} liked your photo '{self.photo.title}'. Currently {self.photo.likes_count+1} likes",
                likes_count=self.photo.likes_count+1,
                photo_id=self.photo.id
            )
