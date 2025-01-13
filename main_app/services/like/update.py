import datetime
from service_objects.services import Service
from django import forms

from main_app.services.like.read import ReadLikeByUserPhotoID
from models_app.models.like.models import Like

class SoftDeleteLike(Service):
    photo_id = forms.IntegerField()
    user_id = forms.IntegerField()

    def process(self) -> Like:
        photo_id = self.cleaned_data['photo_id']
        user_id = self.cleaned_data['user_id']
        like_obj = ReadLikeByUserPhotoID.execute({
            'photo_id': photo_id,
            'user_id': user_id
        })

        if like_obj.deleted_at is not None:
            return like_obj
        else:
            like_obj.deleted_at = datetime.datetime.now()
            like_obj.save()
            return like_obj

class UndoSoftDeletionOfLike(Service):
    photo_id = forms.IntegerField()
    user_id = forms.IntegerField()

    def process(self) -> Like:
        photo_id = self.cleaned_data['photo_id']
        user_id = self.cleaned_data['user_id']
        like_obj = ReadLikeByUserPhotoID.execute({
            'photo_id': photo_id,
            'user_id': user_id
        })

        if like_obj.deleted_at is not None:
            like_obj.deleted_at = None
            like_obj.save()
            return like_obj