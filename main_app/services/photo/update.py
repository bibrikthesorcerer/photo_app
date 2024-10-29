from service_objects.services import Service
from service_objects.fields import ModelField
from celery import current_app

from main_app.tasks.delete_photo.tasks import delete_photo_by_id
from main_app.utils.tasks.utils import scheduled_deletion_tasks
from models_app.models.photo.models import Photo

class SetStatusToTBD(Service):
    photo = ModelField(Photo)

    def process(self):
        photo_obj = self.cleaned_data['photo']
        if photo_obj.status != Photo.TO_BE_DELETED:
            photo_obj.status = Photo.TO_BE_DELETED
            photo_obj.save()
            return True
        else:
            return False
        
class SetStatusToOM(Service):
    photo = ModelField(Photo)

    def process(self):
        photo_obj = self.cleaned_data['photo']
        if photo_obj.status != Photo.ON_MODERATION:
            photo_obj.status = Photo.ON_MODERATION
            photo_obj.save()
            return True
        else:
            return False


class SchedulePhotoDeletion(Service):
    photo = ModelField(Photo)

    def process(self):
        photo_obj = self.cleaned_data['photo']
        status_result = SetStatusToTBD.execute({'photo': photo_obj})
        if status_result is True:
            task_id = delete_photo_by_id.apply_async((photo_obj.id,), countdown=60).id
            scheduled_deletion_tasks.update({photo_obj.id:task_id})
            return True
        else:
            return False
        
class RecoverPhotoBeforeDeletion(Service):
    photo = ModelField(Photo)

    def process(self):
        photo_obj = self.cleaned_data['photo']
        try:
            task_id = scheduled_deletion_tasks[photo_obj.id]
            del scheduled_deletion_tasks[photo_obj.id]
        except KeyError:
            return False
        current_app.control.revoke(task_id, terminate=True)
        SetStatusToOM.execute({'photo': photo_obj})
        return True
