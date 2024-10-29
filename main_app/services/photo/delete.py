from service_objects.services import Service
from service_objects.fields import ModelField
from pathlib import Path
from shutil import rmtree

from models_app.models.photo.models import Photo

class DeletePhotoByID(Service):
    photo = ModelField(Photo)

    def process(self):
        photo_obj = self.cleaned_data['photo']

        if photo_obj.status is Photo.TO_BE_DELETED:
            photo_dir = Path(photo_obj.img.path)
            result =  photo_obj.delete()
            rmtree(photo_dir.parents[1])
            return result
        else:
            return False