from io import BytesIO
import pathlib
import requests
from service_objects.services import ServiceWithResult, ServiceOutcome
from service_objects.errors import ValidationError, Error
from service_objects.fields import ModelField, ListField
from django import forms
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from decouple import config
from django.core.files.images import ImageFile
from django.db.models import Q

from models_app.models import Photo, PhotoVersion, UserProfile, Comment
from api.services.photo_version.create import CreatePhotoVersion
from api.tasks import delete_photo_by_id
from notifications.utils.senders import send_message_to_list_of_users


class UpdatePhoto(ServiceWithResult):
    photo = ModelField(Photo)
    img = forms.ImageField(required=False)
    title = forms.CharField(max_length=64, required=False)
    description = forms.CharField(max_length=256, required=False)

    custom_validations = ["_new_fields_are_present"]

    def process(self):
        self.run_custom_validations()
        self.result = self._update_photo_instance()
        return self

    def _new_fields_are_present(self):
        if len(self.changed_data) <= 1:
            self.add_error(None, ValidationError(message="No values for new fields provided",))
            self.stop_process()
    
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
        self._send_notification_for_comment_authors()
        return self

    def _photo_status_not_tbd(self):
        if self.photo_obj.status == Photo.TO_BE_DELETED:
            self.add_error(None, Error(message="Photo already set to be deleted", response_status = status.HTTP_410_GONE))
            self.stop_process()
    
    def _set_status_to_tbd(self) -> bool:
        self.photo_obj.status = Photo.TO_BE_DELETED
        self.photo_obj.save()

    def _schedule_task(self):
        delete_photo_by_id.apply_async(
            (self.photo_obj.id,),
            countdown=config('PHOTO_DELETION_COUNTDOWN', default=20, cast=int)
        )

    def _get_comment_authors(self) -> list:
        comments = Comment.objects.filter(Q(photo=self.photo_obj) & ~Q(user=self.photo_obj.user))
        idx = comments.values_list("user", flat=True).distinct()
        return idx

    def _send_notification_for_comment_authors(self):
        idx = self._get_comment_authors()
        send_message_to_list_of_users(
            idx,
            "send_notification",
            f"Photo '{self.photo_obj.title}' which you had commented is scheduled to be deleted with all comments you have left."
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
                ValidationError(
                    message="Photo is not set to be deleted",
                    response_status=status.HTTP_400_BAD_REQUEST
                )
            )
            self.stop_process()

    def _recover_photo(self):
        review_ticket = self.photo_obj.review_tickets.first()
        self.photo_obj.status = review_ticket.result if review_ticket else Photo.ON_MODERATION
        self.photo_obj.save()


class ImportPhoto(ServiceWithResult):
    title = forms.CharField(max_length=64)
    description = forms.CharField(max_length=256)
    img = forms.URLField()
    pub_date = forms.DateField(required=False)
    email = forms.EmailField()
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)

    def process(self):
        self.result = self._import_photo()
        return self

    def _import_photo(self):
        photo_author, is_created = self._get_or_create_photo_author()
        img = self._get_photo_img()
        return Photo.objects.create(
            user=photo_author,
            title=self.cleaned_data.get("title"),
            description=self.cleaned_data.get("description"),
            pub_date=self.cleaned_data.get("pub_date"),
            img=img
        )

    def _get_photo_img(self) -> ImageFile:
        response = requests.get(self.cleaned_data.get("img")) # get img from url
        try:
            response.raise_for_status()
        except requests.HTTPError:
            self.add_error("img", ValidationError(message="Unable to fetch image. Check URL and it's accessibility"))
        return ImageFile(
            file=BytesIO(response.content),
            name=self.cleaned_data.get("title"),
        )

    def _get_or_create_photo_author(self) -> UserProfile:
        user, is_created = UserProfile.objects.get_or_create(
            username=self.cleaned_data.get("username"),
            defaults={
                "email": self.cleaned_data.get("email"),
                "first_name": self.cleaned_data.get("first_name"),
                "last_name": self.cleaned_data.get("last_name")
            }
        )
        if is_created:
            user.set_unusable_password()
            user.save()
        return user, is_created


class ImportPhotosList(ServiceWithResult):
    photo_list = ListField()

    def process(self):
        photo_list = self.cleaned_data.get("photo_list")
        for photo_num, photo in enumerate(photo_list):
            self._launch_import_for_photo(photo, photo_num)
        return self

        
    def _launch_import_for_photo(self, photo_info: dict, photo_num):
        try:
            ServiceOutcome(
                ImportPhoto,
                photo_info
            )
        except Exception as e:
            self.add_error(photo_num, e)