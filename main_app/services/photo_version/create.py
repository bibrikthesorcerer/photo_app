from service_objects.services import Service
from service_objects.fields import ModelField

from models_app.models.photo.models import Photo
from models_app.models.photo_version.models import PhotoVersion

class CreatePhotoVersion(Service):
    photo = ModelField(Photo)

    def process(self):
        current_photo = self.cleaned_data['photo']
        return PhotoVersion.objects.create(
            photo = current_photo,
            title = current_photo.title,
            description = current_photo.description,
            pub_date = current_photo.pub_date,
            status = current_photo.status, 
            img = current_photo.img,
        )
