from service_objects.services import Service
from service_objects.fields import ModelField

from main_app.tasks.delete_photo.tasks import delete_photo_by_id
from models_app.models.photo.models import Photo

class SchedulePhotoDeletion(Service):
    photo = ModelField(Photo)

    def process(self):
        photo_obj = self.cleaned_data['photo']
        if photo_obj.status == Photo.TO_BE_DELETED:
            return False
        
        photo_obj.status = Photo.TO_BE_DELETED
        photo_obj.save()
        delete_photo_by_id.apply_async((photo_obj.id,), countdown=20)
        return True

 
class RecoverPhotoBeforeDeletion(Service):
    photo = ModelField(Photo)

    def process(self):
        photo_obj = self.cleaned_data['photo']
        if photo_obj.status != Photo.TO_BE_DELETED:
            return False
        photo_obj.status = Photo.ON_MODERATION
        photo_obj.save()
        return True
