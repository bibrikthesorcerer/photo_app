from django import forms
from django.db.models import Prefetch
from django.db.models import Q
from service_objects.services import ServiceWithResult

from models_app.models.comment.models import Comment


class RetrieveComment(ServiceWithResult):
    """
    Retrieves Comment object with info about user and children comments

    Parameters
    ----------
          comment_id (int): primary key of an object being retrieved
    """

    comment_id = forms.IntegerField()

    def process(self) -> Comment:
        self.result = self._get_comment_instance()
        return self.result

    def _get_comment_instance(self) -> Comment:
        self._get_comments_manager()
        self._add_extra_params()
        comment_id = self.cleaned_data.get("comment_id")
        return self.objects.get(pk=comment_id)

    def _add_extra_params(self):
        self._prefetch_children()
        self._select_related_user()

    def _get_comments_manager(self):
        self.objects = Comment.objects

    def _prefetch_children(self):
        children_query = Comment.objects.filter(
            Q(deleted_at=None) | (Q(text__exact="DELETED") & ~Q(deleted_at=None))
        )
        self.objects = self.objects.prefetch_related(
            Prefetch("children", queryset=children_query)
        )

    def _select_related_user(self):
        self.objects = self.objects.select_related("user")
