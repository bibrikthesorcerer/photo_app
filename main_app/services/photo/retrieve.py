from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from django.db.models import Count, QuerySet, Exists, OuterRef
from django import forms
from django.db.models import Q

from models_app.models import Photo, Like, UserProfile

class RetrievePhoto(ServiceWithResult):
    """
    Retrieves Photo object from database 

    Parameters
    ----------
        photo_id (int): ID of a photo being retrieved
        user (UserProfile, optional): used to calculate whether or not retrieving photo liked by user
    """
    photo_id = forms.IntegerField()
    user = ModelField(UserProfile, required=False)

    def process(self) -> Photo:
        objects = self._all_photos_query()
        objects = self._count_likes_and_comments(objects)
        objects = self._select_related_user(objects)
        objects = self._is_liked_by_user(objects)
        self.result = self._get_photo_instance(objects)
        return self.result
    
    def _get_photo_instance(self, objects: QuerySet[Photo]) -> QuerySet[Photo]:
        pk = self.cleaned_data.get('photo_id')
        return objects.get(pk=pk)

    def _all_photos_query(self):
        return Photo.objects.all()

    def _is_liked_by_user(self, objects: QuerySet[Photo]) -> QuerySet[Photo]:
        user = self.cleaned_data.get('user')
        if not user:
                return objects
        
        like_subquery = Like.objects.filter(
                photo=OuterRef('pk'),
                user=user,
                deleted_at=None
        )
        return objects.annotate(is_liked=Exists(like_subquery))
    
    def _count_likes_and_comments(self, objects: QuerySet[Photo]) -> QuerySet[Photo]:
        return objects.annotate(
                likes_count=Count('like', filter=Q(like__deleted_at=None), distinct=True), 
                comments_count=Count('comment', filter=Q(comment__deleted_at=None), distinct=True))

    def _select_related_user(self, objects: QuerySet[Photo]) -> QuerySet[Photo]:
        return objects.select_related('user')
