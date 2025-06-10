from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from service_objects.errors import ValidationError, NotFound
from rest_framework import status
from django import forms

from models_app.models import UserProfile, Comment, Photo


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
            self.related_photo = Photo.objects.get(id=photo_id)
        except Photo.DoesNotExist:
            self.add_error("photo_id", NotFound(message="Photo with given id not found"))
            self.stop_process()
