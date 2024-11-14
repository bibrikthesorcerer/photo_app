from django.forms import IntegerField
from service_objects.services import Service

from main_app.services.photo.read import ReadPhotoByID
from models_app.models.photo_version.models import PhotoVersion

class CreatePhotoVersion(Service):
    photo_id = IntegerField()

    def process(self):
        current_photo = ReadPhotoByID.execute({'photo_id': self.cleaned_data['photo_id']})
        return PhotoVersion.objects.create(
            photo = current_photo,
            title = current_photo.title,
            description = current_photo.description,
            pub_date = current_photo.pub_date,
            status = current_photo.status, 
            img = current_photo.img,
        )
