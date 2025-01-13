from service_objects.services import Service
from django import forms
from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist

from models_app.models.like.models import Like

class ReadLikeByUserPhotoID(Service):
    photo_id = forms.IntegerField()
    user_id = forms.IntegerField()

    def process(self) -> QuerySet:
        photo_id = self.cleaned_data['photo_id']
        user_id = self.cleaned_data['user_id']
        return Like.objects.get(photo=photo_id, user=user_id)
    
class CheckIfLikeSoftDeleted(Service):
    photo_id = forms.IntegerField()
    user_id = forms.IntegerField()

    def process(self) -> bool:
        photo_id = self.cleaned_data['photo_id']
        user_id = self.cleaned_data['user_id']
        try:
            like_obj = ReadLikeByUserPhotoID.execute({
                'photo_id': photo_id, 
                'user_id': user_id
                })
            if like_obj.deleted_at is not None:
                return True
            else:
                return False
        except ObjectDoesNotExist:
            return False