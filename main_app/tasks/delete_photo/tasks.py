from celery import shared_task

from main_app.services.photo.delete import DeletePhotoByID

@shared_task
def delete_photo_by_id(photo_id):
    return DeletePhotoByID.execute({'photo_id': photo_id})