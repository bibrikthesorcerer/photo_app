from service_objects.services import ServiceWithResult
from django import forms

from models_app.models import Photo

class DeletePhoto(ServiceWithResult):
    """
    Deletes Photo object based on a given ID  
    Only photo with `TO_BE_DELETED` status can be deleted

    Parameters
    ----------
        photo_id (int)
    """
    photo_id = forms.IntegerField()

    def process(self):
        photo_id = self.cleaned_data.get('photo_id')
        photos = Photo.objects.filter(id=photo_id, status=Photo.TO_BE_DELETED)
        self.result = photos.delete()
        return self.result