from service_objects.services import Service
from models_app.models import PhotoVersion
from django.db.models import QuerySet
from django import forms

class ReadPhotoVersionsByPhotoID(Service):
    """
    Lists photo versions associated with photo in order of creation
    Parameters
    ----------
        photo_id (int): id of a associated photo
    """
    photo_id = forms.IntegerField()

    def process(self) -> QuerySet[PhotoVersion]:
        return PhotoVersion.objects.filter(photo=self.cleaned_data.get('photo_id')).order_by('-created_at')