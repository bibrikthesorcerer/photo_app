from service_objects.services import Service
from models_app.models import Photo
from django import forms

class ReadAllPhotos(Service):
    def process(self):
            self.photos = Photo.objects.all()
            return self.photos

class ReadPhotoByUserID(Service):
      user_id = forms.IntegerField()
      def process(self):
            return Photo.objects.filter(user=self.cleaned_data['user_id'])