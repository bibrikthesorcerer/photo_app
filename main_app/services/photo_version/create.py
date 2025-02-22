from django.forms import IntegerField
from service_objects.services import ServiceWithResult

from main_app.services import RetrievePhoto
from models_app.models import PhotoVersion

class CreatePhotoVersion(ServiceWithResult):
    """
    Creates PhotoVersion based on photo id

    Parameters
    ----------
        photo_id (int): id of a photo being archived
    """
    photo_id = IntegerField()

    def process(self) -> PhotoVersion:
        photo_id = self.cleaned_data['photo_id']
        current_photo = RetrievePhoto.execute({"photo_id": photo_id})

        last_version = PhotoVersion.objects.filter(photo_id=photo_id).order_by('-iteration').first()
        next_iteration = last_version.iteration + 1 if last_version else 1
        
        self.result = PhotoVersion.objects.create(
            photo = current_photo,
            title = current_photo.title,
            description = current_photo.description,
            iteration = next_iteration,
            img = current_photo.img,
        )

        return self.result
