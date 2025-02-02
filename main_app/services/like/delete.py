from service_objects.services import Service
from django import forms

from models_app.models import Like

class SoftDeleteLike(Service):
    photo_id = forms.IntegerField()
    user_id = forms.IntegerField()

    def process(self) -> Like:
        photo_id = self.cleaned_data['photo_id']
        user_id = self.cleaned_data['user_id']
        like_obj = Like.objects.filter(photo=photo_id, user=user_id).delete()
        return like_obj.first()