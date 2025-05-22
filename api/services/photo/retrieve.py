from service_objects.services import ServiceWithResult
from django import forms
from django.db.models import Count, Q, Exists, OuterRef
from rest_framework import status

from models_app.models import Photo, Like

class RetrievePhoto(ServiceWithResult):
    photo_id = forms.IntegerField()
    user_id = forms.IntegerField(required=False)

    def process(self):
        self.result = self._get_photo_instance()
        return self
    
    def _get_photo_instance(self):
        self._get_photos_manager()
        self._add_extra_params()
        try:
            return self.objects.get(id=self.cleaned_data.get('photo_id'))
        except Photo.DoesNotExist:
            self.add_error("photo_id", "Photo with given id not found")
            self.response_status = status.HTTP_404_NOT_FOUND
            self.stop_process()

    def _get_photos_manager(self):
        self.objects = Photo.objects

    def _add_extra_params(self):
        self._prefetch_related()
        self._select_related()
        self._count_likes_and_comments()
        self._is_liked_by_user()

    def _prefetch_related(self):
        self.objects = self.objects.prefetch_related('review_tickets')

    def _select_related(self):
        self.objects = self.objects.select_related('user')

    def _count_likes_and_comments(self):
        self.objects = self.objects.annotate(
            likes_count=Count("like", filter=Q(like__deleted_at=None), distinct=True),
            comments_count=Count("comment", filter=(Q(comment__deleted_at=None)), distinct=True)
        )

    def _is_liked_by_user(self):
        user_id = self.cleaned_data.get("user_id")
        if not user_id:
            return

        like_subquery = Like.objects.filter(
            photo=OuterRef("pk"), user_id=user_id, deleted_at=None
        )
        self.objects = self.objects.annotate(is_liked=Exists(like_subquery))