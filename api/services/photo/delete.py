from service_objects.services import ServiceWithResult
from django import forms

from models_app.models import Photo


class DeletePhoto(ServiceWithResult):
    photo_id = forms.IntegerField()

    def process(self):
        self.result = self._delete_photo()
        return self
    
    def _delete_photo(self):
        photo_id = self.cleaned_data.get('photo_id')
        query = Photo.objects.filter(id=photo_id, status=Photo.TO_BE_DELETED)
        return query.delete()