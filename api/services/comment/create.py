from service_objects.services import ServiceWithResult, ServiceOutcome
from service_objects.fields import ModelField
from service_objects.errors import ValidationError, NotFound
from rest_framework import status
from django import forms

from models_app.models import UserProfile, Comment, Photo
from api.services.photo.retrieve import RetrievePhoto
from notifications.utils.senders import send_message_to_list_of_users


class CreateComment(ServiceWithResult):
    photo_id = forms.IntegerField()
    parent_id = forms.IntegerField(required=False)
    user = ModelField(UserProfile)
    text = forms.CharField(max_length=256)

    custom_validations = ["_parent_exists", "_photo_exists", "_photo_has_parent_comment"]

    def process(self):
        self.run_custom_validations()
        self.result = Comment(
            parent=self.parent_comment,
            photo=self.related_photo,
            user=self.cleaned_data.get('user'),
            text=self.cleaned_data.get('text')
        )
        self.result.save()
        self._send_notification_for_photo_author()
        return self

    def _photo_has_parent_comment(self):
        if self.parent_comment is not None \
            and self.parent_comment.photo_id != self.related_photo.id:
            self.add_error(None,ValidationError(message="Parent comment's photo id and photo_id must match",))
            self.stop_process()

    def _parent_exists(self):
        parent_id = self.cleaned_data.get("parent_id")
        try:
            self.parent_comment = Comment.objects.get(id=parent_id) if parent_id else None
        except Comment.DoesNotExist:
            self.add_error("parent_id", NotFound(message="Parent comment with given id not found"))
            self.stop_process()
    
    def _photo_exists(self):
        photo_id = self.cleaned_data.get("photo_id")
        try:
            self.related_photo = ServiceOutcome(
                RetrievePhoto,
                self.cleaned_data
            ).result
        except Photo.DoesNotExist:
            self.add_error("photo_id", NotFound(message="Photo with given id not found"))
            self.stop_process()

    def _send_notification_for_photo_author(self):
        user = self.cleaned_data.get('user')
        if user == self.related_photo.user.id:
            return
        send_message_to_list_of_users(
            [self.related_photo.user.id],
            'notify_comment',
            f"User {user} commented on your photo '{self.related_photo.title}'. Currently {self.related_photo.comments_count} comments",
            comments_count=self.related_photo.comments_count,
            photo_id=self.related_photo.id
        )
