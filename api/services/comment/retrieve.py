from service_objects.services import ServiceWithResult
from service_objects.errors import Error
from rest_framework import status
from django import forms
from django.db.models import Q, Prefetch

from models_app.models import Comment


class RetrieveComment(ServiceWithResult):
    comment_id = forms.IntegerField()

    def process(self):
        self.result = self._get_comment_instance()
        return self
    
    def _get_comment_instance(self) -> Comment:
        self._get_comments_manager()
        self._add_extra_params()
        comment_id = self.cleaned_data.get("comment_id")
        try:
            return self.objects.get(id=comment_id)
        except Comment.DoesNotExist as e:
            self.add_error("comment_id", Error(message="Comment with given id not found"))
            self.response_status = status.HTTP_404_NOT_FOUND
            self.stop_process()

    def _get_comments_manager(self):
        self.objects = Comment.objects

    def _add_extra_params(self):
        self._prefetch_children()
        self._select_related_user()

    def _prefetch_children(self):
        children_query = Comment.objects.filter(
            Q(deleted_at=None) | (Q(text__exact="DELETED") & ~Q(deleted_at=None))
        )
        self.objects = self.objects.prefetch_related(
            Prefetch("children", queryset=children_query)
        )

    def _select_related_user(self):
        self.objects = self.objects.select_related("user")