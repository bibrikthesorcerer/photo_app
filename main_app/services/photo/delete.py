from service_objects.services import Service
from django import forms

from models_app.models.photo.models import Photo

class DeletePhotoByID(Service):
    photo_id = forms.IntegerField()

    def _delete_img_files(self, objects):
        for obj in objects:
            obj.img.delete()

    def process(self):
        photo_id = self.cleaned_data['photo_id']
        photos = Photo.objects.filter(id=photo_id, status=Photo.TO_BE_DELETED)
        self._delete_img_files(photos)
        return photos.delete()