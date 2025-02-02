from service_objects.services import Service
from service_objects.fields import ModelField
from django import forms

from main_app.tasks.delete_photo.tasks import delete_photo_by_id
from models_app.models.photo.models import Photo
        
class SetStatus(Service):
    STATUS_CHOICES = [
        ('TBD', ''),
        ('APR', ''),
        ('DEN', ''),
        ('OM', ''),
    ]

    photo = ModelField(Photo)
    status = forms.ChoiceField(choices=STATUS_CHOICES)

    def process(self):
        photo_obj = self.cleaned_data['photo']
        status = self.cleaned_data['status']
        if photo_obj.status != status:
            photo_obj.status = status
            photo_obj.save()
            return True
        else:
            return False


class SchedulePhotoDeletion(Service):
    photo = ModelField(Photo)

    def process(self):
        photo_obj = self.cleaned_data['photo']
        if photo_obj.status == 'TBD':
            return False
        
        photo_obj.status = 'TBD'
        photo_obj.save()
        delete_photo_by_id.apply_async((photo_obj.id,), countdown=20)
        return True

 
class RecoverPhotoBeforeDeletion(Service):
    photo = ModelField(Photo)

    def process(self):
        photo_obj = self.cleaned_data['photo']
        if photo_obj.status != 'TBD':
            return False
        photo_obj.status = 'OM'
        photo_obj.save()
        return True
