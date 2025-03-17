from copy import deepcopy
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from decouple import config
from django import forms
import pathlib

from main_app.tasks import delete_photo_by_id
from models_app.admin.photo.forms import PhotoForm
from models_app.models import Photo
from main_app.services.review_ticket import UpdateReviewTicketWithVersion
from main_app.services.photo_version import CreatePhotoVersion


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
        new_photo = self.cleaned_data.get('new_photo')
        old_photo = self.cleaned_data.get('old_photo')
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
        photo_obj = self.cleaned_data.get('photo')
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
        photo_obj = self.cleaned_data.get('photo')
        if photo_obj.status != Photo.TO_BE_DELETED:
            self.result = False
            return self.result
        
        # get review ticket associated with photo
        ticket = photo_obj.review_tickets.first()
        photo_obj.status = ticket.result if ticket else Photo.ON_MODERATION
        photo_obj.save()
        self.result = True
        return self.result


class UpdatePhoto(ServiceWithResult):
    """
    Updates Photo object, creates PhotoVersion to archive last state of Photo.

    Parameters
    ----------
        title (str, optional): new title
        description (str, optional): new description
        img (Image, optional): new Image file
        photo (Photo): an object being archived
    """
    title = forms.CharField(max_length=64,required=False)
    description = forms.CharField(max_length=256,required=False)
    img = forms.ImageField(required=False)
    photo = ModelField(Photo)

    def _collect_form_data(self) -> dict[str, str]:
        post = {
            "title": self.cleaned_data.get("title"),
            "description": self.cleaned_data.get("description"),
            "img": self.cleaned_data.get("img")
        }
        files = {"img": self.cleaned_data.get("img")}
        return (post, files)
    
    def process(self) -> Photo|None:
        photo = self.cleaned_data.get("photo")
        form = PhotoForm(*self._collect_form_data(), instance=deepcopy(photo))
        self.result = None
        if form.is_valid():
            version = CreatePhotoVersion.execute({"photo_id":photo.id})
            UpdateReviewTicketWithVersion.execute({
                "photo_id": photo.id,
                "photo_version_id": version.id
            })
            ManageOldImage.execute({"new_photo":form.instance, "old_photo": photo})
            form.instance.status = Photo.ON_MODERATION
            form.instance.pub_date = None
            self.result = form.save()
        return self.result