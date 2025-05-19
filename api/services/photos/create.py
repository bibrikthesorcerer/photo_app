from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from django import forms
from rest_framework import status

from models_app.models import UserProfile, Photo

class CreatePhoto(ServiceWithResult):
    img = forms.ImageField()
    title = forms.CharField(max_length=64)
    description = forms.CharField(max_length=256)
    user = ModelField(UserProfile)

    def process(self):
        self.result = self._create_photo_instance()
        return self
    
    def _create_photo_instance(self):
        self._collect_inputs()
        return Photo.objects.create(
            user=self.user,
            title=self.title,
            description=self.description,
            img=self.img
        )
    
    def _collect_inputs(self):
        self.user = self.cleaned_data.get('user')
        self.title = self.cleaned_data.get('title')
        self.description = self.cleaned_data.get('description')
        self.img = self.cleaned_data.get('img')