from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from django.db.models import QuerySet

from models_app.models import Like, Photo, UserProfile

class UpdateOrCreateLike(ServiceWithResult):
    """
    Updates Like object if it is soft deleted
    or creates new Like object if there are no objects with given parameters

    Parameters
    ----------
        photo (Photo): photo associated with like
        user (UserProfile): user associated with like
    """
    photo = ModelField(Photo)
    user = ModelField(UserProfile)

    def process(self) -> QuerySet[Like]:
        photo = self.cleaned_data.get('photo')
        user = self.cleaned_data.get('user')
        self.result, _created = Like.objects.update_or_create(
            photo=photo,
            user=user,
            defaults={"deleted_at": None},
        )
        return self.result