from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from django import forms

from models_app.models import PhotoVersion, Photo
from api.services.photo.retrieve import RetrievePhoto

class CreatePhotoVersion(ServiceWithResult):
    photo = ModelField(Photo)

    def process(self) -> PhotoVersion:
        photo = self.cleaned_data.get("photo")
        last_version = PhotoVersion.objects.filter(photo_id=photo.id).order_by('-iteration').first()
        next_iteration = last_version.iteration + 1 if last_version else 1
        
        self.result = PhotoVersion.objects.create(
            photo = photo,
            title = photo.title,
            description = photo.description,
            iteration = next_iteration,
            img = photo.img,
        )

        return self
