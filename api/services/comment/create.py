from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from rest_framework import status
from django import forms
from django.core.exceptions import ObjectDoesNotExist

from models_app.models import UserProfile, Comment, Photo


class CreateComment(ServiceWithResult):
    photo_id = forms.IntegerField()
    parent_id = forms.IntegerField(required=False)
    user = ModelField(UserProfile)
    text = forms.CharField(max_length=256)

    custom_validations = ["_photo_has_parent_comment"]

    def _photo_has_parent_comment(self):
        try:
            if self.parent_comment is not None \
                and self.parent_comment.photo_id != self.related_photo.id:
                self.add_error(None, "Parent comment's photo id and photo_id must match")
                raise

        except Comment.DoesNotExist:
            self.add_error("parent_id", "Parent comment with given id not found")
            self.response_status = status.HTTP_400_BAD_REQUEST
            self.stop_process()
        except Photo.DoesNotExist:
            self.add_error("photo_id", "Photo with given id not found")
            self.response_status = status.HTTP_400_BAD_REQUEST
            self.stop_process()
        except Exception:
            self.response_status = status.HTTP_400_BAD_REQUEST
            self.stop_process()

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
    
    @property
    def parent_comment(self) -> Comment|None:
        parent_id = self.cleaned_data.get('parent_id')
        if not parent_id:
            return None
        return Comment.objects.get(id=parent_id)
    
    @property
    def related_photo(self) -> Photo:
        photo_id = self.cleaned_data.get('photo_id')
        return Photo.objects.get(id=photo_id)
