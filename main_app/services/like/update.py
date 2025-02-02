from service_objects.services import Service
from service_objects.fields import ModelField
from django import forms

from models_app.models import Like

class UndoSoftDeletionOfLike(Service):
    like = ModelField(Like)
    def process(self) -> Like:
        like_obj = self.cleaned_data['like']
        if like_obj.deleted_at is not None:
            like_obj.deleted_at = None
            like_obj.save()
        return like_obj