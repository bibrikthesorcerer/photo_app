from service_objects.services import Service
from models_app.models import Photo
from django.db.models import Count, QuerySet
from django import forms

class ReadAllPhotos(Service):
    
    def process(self) -> QuerySet:
            return Photo.objects.all()

class ReadPhotoByUserID(Service):
      user_id = forms.IntegerField()

      def process(self) -> QuerySet:
            return Photo.objects.filter(user=self.cleaned_data['user_id'])
      
class ReadPhotoByID(Service):
      photo_id = forms.IntegerField()

      def process(self) -> Photo:
            return Photo.objects.get(pk=self.cleaned_data['photo_id'])
      
class ReadAllPhotosWithLikes(Service):

      def process(self) -> QuerySet:
            photos = ReadAllPhotos.execute({})
            return photos.annotate(likes_count=Count('like'))