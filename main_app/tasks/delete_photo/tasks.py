from celery import shared_task

from main_app.services.photo.delete import DeletePhotoByID
from main_app.services.photo.read import ReadPhotoByID
from main_app.utils.tasks.utils import scheduled_deletion_tasks

@shared_task
def delete_photo_by_id(photo_id):
    try:
        # remove task_id from dict of all scheduled del tasks
        # so it cannot be canceled
        del scheduled_deletion_tasks[photo_id]
    except KeyError:
        return False
    
    photo = ReadPhotoByID.execute({'photo_id': photo_id})
    return DeletePhotoByID.execute({'photo': photo})