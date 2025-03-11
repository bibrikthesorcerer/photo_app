from service_objects.services import ServiceWithResult
from django import forms

from models_app.models import Like

class DeleteLike(ServiceWithResult):
    """
    Deletes Like object (soft deletion is used)

    Parameters
    ----------
        photo_id (int): id of a photo to which user left like
        user_id (int): id of a user who left like
    """
    photo_id = forms.IntegerField()
    user_id = forms.IntegerField()

    def process(self) -> Like:
        photo_id = self.cleaned_data.get('photo_id')
        user_id = self.cleaned_data.get('user_id')
        like_obj = Like.objects.filter(photo=photo_id, user=user_id).delete()
        self.result = like_obj.first()
        return self.result