from service_objects.services import Service
from models_app.models import PhotoVersion
from django.db.models import QuerySet
from django import forms

class ReadPhotoVersionsByPhotoID(Service):
    photo_id = forms.IntegerField()

    def process(self) -> QuerySet:
        return PhotoVersion.objects.filter(photo=self.cleaned_data['photo_id']).order_by('-created_at')