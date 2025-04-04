from django import forms
from django.db.models import Count
from django.db.models import Exists
from django.db.models import OuterRef
from django.db.models import Q
from django.db.models import QuerySet
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from models_app.models import Like
from models_app.models import Photo
from models_app.models import UserProfile


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
        self.result = self._get_photo_instance()
        return self.result

    def _get_photo_instance(self) -> Photo:
        self._get_photos_manager()
        self._add_extra_params()
        pk = self.cleaned_data.get("photo_id")
        return self.objects.get(pk=pk)

    def _get_photos_manager(self):
        self.objects = Photo.objects
    
    def _add_extra_params(self):
        self._count_likes_and_comments()
        self._select_related_user()
        self._prefetch_related()
        self._is_liked_by_user()


    def _is_liked_by_user(self):
        user = self.cleaned_data.get("user")
        if not user:
            return

        like_subquery = Like.objects.filter(
            photo=OuterRef("pk"), user=user, deleted_at=None
        )
        self.objects = self.objects.annotate(is_liked=Exists(like_subquery))

    def _count_likes_and_comments(self):
        self.objects = self.objects.annotate(
            likes_count=Count("like", filter=Q(like__deleted_at=None), distinct=True),
            comments_count=Count(
                "comment", filter=Q(comment__deleted_at=None), distinct=True
            ),
        )

    def _select_related_user(self):
        self.objects = self.objects.select_related("user")

    def _prefetch_related(self):
        self.objects = self.objects.prefetch_related("review_tickets")
