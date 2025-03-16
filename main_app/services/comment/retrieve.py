from service_objects.services import ServiceWithResult
from django import forms
from django.db.models import QuerySet, Prefetch, Q

from models_app.models.comment.models import Comment

class RetrieveComment(ServiceWithResult):
    """
      Retrieves Comment object with info about user and children comments

      Parameters
      ----------
            pk (int): primary key of an object being retrieved
      """
    pk = forms.IntegerField()

    def process(self):
        objects = self._all_comments_query()
        objects = self._prefetch_children(objects)
        objects = self._select_related_user(objects)
        objects = self._get_data(objects)
        self.result = objects
        return self.result
    
    def _all_comments_query(self) -> QuerySet:
        return Comment.objects.all()
    
    def _get_data(self, objects: QuerySet) -> Comment:
        pk = self.cleaned_data.get('pk')
        return objects.get(pk=pk)
    
    def _prefetch_children(self, objects: QuerySet) -> QuerySet:
        children_query = Comment.objects.filter(Q(deleted_at=None) 
                                                | (Q(text__exact="DELETED") & ~Q(deleted_at=None)))
        return objects.prefetch_related(Prefetch('children', queryset=children_query))
    
    def _select_related_user(self, objects: QuerySet) -> QuerySet:
        return objects.select_related('user')
