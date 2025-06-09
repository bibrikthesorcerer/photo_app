import pathlib
from service_objects.services import ServiceWithResult
from service_objects.errors import Error
from service_objects.fields import ModelField
from django import forms
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from decouple import config

from models_app.models import Photo, PhotoVersion
from api.services.photo_version.create import CreatePhotoVersion
from api.tasks import delete_photo_by_id


class UpdatePhoto(ServiceWithResult):
    photo = ModelField(Photo)
    img = forms.ImageField(required=False)
    title = forms.CharField(max_length=64, required=False)
    description = forms.CharField(max_length=256, required=False)

    custom_validations = ["_new_fields_are_present"]

    def _new_fields_are_present(self):
        if len(self.changed_data) <= 1:
            self.add_error(None, Error(
                message="No values for new fields provided",
                response_status = status.HTTP_400_BAD_REQUEST
                )
            )
            self.response_status = status.HTTP_400_BAD_REQUEST
            self.stop_process()

    def process(self):
        self.run_custom_validations()
        self.result = self._update_photo_instance()
        return self
    
    def _update_photo_instance(self):
        self._get_photo_instance()
        self._create_version()
        self._assign_ticket_to_version()
        self._set_new_photo_fields()
        self.photo_obj.save()
        return self.photo_obj
    
    def _set_new_photo_fields(self):
        title = self.cleaned_data.get('title')
        if title:
            self.photo_obj.title = title
        description = self.cleaned_data.get('description')
        if description:
            self.photo_obj.description = description
        img = self.cleaned_data.get('img')
        if img and self.photo_obj.img != img:
            file_path = pathlib.Path(self.photo_obj.img.path)
            file_path.unlink(missing_ok=True)
            self.photo_obj.img = img
        self.photo_obj.status = Photo.ON_MODERATION
        self.photo_obj.pub_date = None

    def _get_photo_instance(self) -> Photo:
        self.photo_obj = self.cleaned_data.get('photo')
        
    def _create_version(self):
        self.photo_version = CreatePhotoVersion.execute({"photo": self.photo_obj}).result

    def _assign_ticket_to_version(self):
        if not self.photo_obj.review_tickets.all():
            return 
        ticket = self.photo_obj.review_tickets.all()[0]
        ticket.object_id = self.photo_version.id
        ticket.content_type = ContentType.objects.get_for_model(PhotoVersion)
        ticket.save(update_fields=['object_id', 'content_type'])


class SchedulePhotoDeletion(ServiceWithResult):
    photo = ModelField(Photo)

    custom_validations = ["_photo_status_not_tbd"]

    def process(self):
        self.photo_obj = self.cleaned_data.get("photo")
        self.run_custom_validations()
        self._set_status_to_tbd()
        self._schedule_task()
        return self

    def _photo_status_not_tbd(self):
        if self.photo_obj.status == Photo.TO_BE_DELETED:
            self.add_error(None, Error(message="Photo already set to be deleted"))
            self.response_status = status.HTTP_410_GONE
            self.stop_process()
    
    def _set_status_to_tbd(self) -> bool:
        self.photo_obj.status = Photo.TO_BE_DELETED
        self.photo_obj.save()

    def _schedule_task(self):
        delete_photo_by_id.apply_async(
            (self.photo_obj.id,),
            countdown=config('PHOTO_DELETION_COUNTDOWN', default=20, cast=int)
        )

class RecoverPhotoFromDeletion(ServiceWithResult):
    photo = ModelField(Photo)

    custom_validations = ["_photo_status_is_tbd"]

    def process(self):
        self.photo_obj = self.cleaned_data.get('photo')
        self.run_custom_validations()
        self._recover_photo()
        return self

    def _photo_status_is_tbd(self):
        if self.photo_obj.status != Photo.TO_BE_DELETED:
            self.add_error(
                None,
                Error(
                    message="Photo is not set to be deleted",
                    response_status=status.HTTP_400_BAD_REQUEST
                )
            )
            self.response_status = status.HTTP_400_BAD_REQUEST
            self.stop_process()

    def _recover_photo(self):
        review_ticket = self.photo_obj.review_tickets.first()
        self.photo_obj.status = review_ticket.result if review_ticket else Photo.ON_MODERATION
        self.photo_obj.save()