from service_objects.services import Service
from models_app.models import Photo
from django.db.models import Count, QuerySet
from django import forms
from django.db.models import Q
from django.core.exceptions import FieldError

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
      
class ReadAllPhotosWithComments(Service):

      def process(self) -> QuerySet:
            photos = ReadAllPhotos.execute({})
            return photos.annotate(comments_count=Count('comment'))
      
class ReadAllPhotosWithLikesAndComments(Service):
      
      def process(self) -> QuerySet:
            photos = ReadAllPhotos.execute({})
            return photos.annotate(likes_count=Count('like'), comments_count=Count('comment'))

class ReadAllPhotosWithUsers(Service):

      def process(self) -> QuerySet:
            photos = ReadAllPhotos.execute({})
            return photos.select_related('user')

class ReadPhotosIDWithEntry(Service):
      entry = forms.CharField(required=False)

      def process(self) -> list:
            entry = self.cleaned_data['entry']
            photos = ReadAllPhotosWithUsers.execute({})
            photo_query = photos.filter(
                  Q(title__icontains=entry) | 
                  Q(description__icontains=entry) | 
                  Q(user__username__icontains=entry)
                  )
            photo_ids =  photo_query.values_list('id') # returns list of tuples
            photo_ids = [elem[0] for elem in photo_ids]
            return photo_ids

class ReadPhotosAndOrder(Service):
      order = forms.CharField()

      def process(self):
            order = self.cleaned_data['order']
            photos = ReadAllPhotosWithLikesAndComments.execute({})
            try:
                  ordered_photos = photos.order_by(order)
                  photo_ids =  ordered_photos.values_list('id')
                  photo_ids = [elem[0] for elem in photo_ids]
                  return photo_ids
            except FieldError:
                  return []