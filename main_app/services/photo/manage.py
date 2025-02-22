from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from decouple import config
import pathlib

from main_app.tasks import delete_photo_by_id
from models_app.models import Photo


class ManageOldImage(ServiceWithResult):
    """
    Manages removal of old Photo image file if it was changed

    Parameters
    ----------
        new_photo (Photo): new Photo instance
        old_photo (Photo): old Photo instance
    """
    new_photo = ModelField(Photo)
    old_photo = ModelField(Photo)

    def process(self) -> bool:
        new_photo = self.cleaned_data['new_photo']
        old_photo = self.cleaned_data['old_photo']
        if new_photo.img != old_photo.img:
            file_path = pathlib.Path(old_photo.img.path)
            file_path.unlink(missing_ok=True)
            self.result = True
        
        self.result = False
        return self.result


class SchedulePhotoDeletion(ServiceWithResult):
    """
    Schedules deletion of Photo by setting status to `TO_BE_DELETED` and creating delayed celery task

    Parameters
    ----------
        photo (Photo): an object scheduling to be deleted
    """
    photo = ModelField(Photo)

    def process(self) -> bool:
        photo_obj = self.cleaned_data['photo']
        if photo_obj.status == Photo.TO_BE_DELETED:
            self.result = False
            return self.result
        
        photo_obj.status = Photo.TO_BE_DELETED
        photo_obj.save()
        delete_photo_by_id.apply_async((photo_obj.id,), countdown=config('PHOTO_DELETION_COUNTDOWN', cast=int))
        self.result = True
        return self.result

 
class RecoverPhotoBeforeDeletion(ServiceWithResult):
    """
    Recovers Photo from being deleted by changing it's status

    Parameters
    ----------
        photo (Photo): an object being recovered
    """
    photo = ModelField(Photo)

    def process(self) -> bool:
        photo_obj = self.cleaned_data['photo']
        if photo_obj.status != Photo.TO_BE_DELETED:
            self.result = False
            return self.result
        
        photo_obj.status = Photo.ON_MODERATION
        photo_obj.save()
        self.result = True
        return self.result
