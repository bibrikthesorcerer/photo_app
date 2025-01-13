from service_objects.services import Service
from service_objects.fields import ModelField

from models_app.models.like.models import Like
from models_app.models.photo.models import Photo
from models_app.models.user_profile.models import UserProfile

class CreateLikeFromUserPhotoID(Service):
    photo = ModelField(Photo)
    user = ModelField(UserProfile)

    def process(self) -> Like:
        return Like.objects.create(
            photo = self.cleaned_data['photo'],
            user = self.cleaned_data['user'],
        )