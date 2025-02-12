from typing import Union
from service_objects.services import ServiceWithResult
from django import forms
from django.db.models import QuerySet, Prefetch
from decouple import config

from main_app.services.comment.retrieve import RetrieveComment
from models_app.models.comment.models import Comment

class ListComments(ServiceWithResult):
    """
      Lists Comment objects or QuerySets with info about users and children comments

      Parameters
      ----------
            include_deleted (bool): whether or not to give out deleted comments
      """
    include_deleted = forms.BooleanField(required=False)
    photo = forms.IntegerField(required=False)
    parent__isnull = forms.BooleanField(required=False)
    
    def process(self) -> Union[QuerySet, Comment]:
        objects = self._all_comments_query()
        objects = self._prefetch_children(objects)
        objects =  self._select_related_user(objects)
        objects = self._order_by_date(objects)
        objects = self._filter_deleted(objects)
        objects = self._filter_data(objects)

        self.result = objects
        return self.result
    
    def _order_by_date(self, objects: QuerySet) -> QuerySet:
        return objects.order_by('-pub_date')
    
    
    def _filter_deleted(self, objects: QuerySet) -> QuerySet:
        include_deleted = self.cleaned_data['include_deleted']
        if not include_deleted:
            return objects.filter(deleted_at=None)
        else:
            return objects
        
    def _filter_data(self, objects: QuerySet) -> QuerySet:
        photo = self.cleaned_data['photo']
        parent__isnull = self.cleaned_data['parent__isnull']
        return objects.filter(
            photo=photo,
            parent__isnull=parent__isnull
            )
    
    def _all_comments_query(self) -> QuerySet:
        return Comment.objects.all()
    
    def _prefetch_children(self, objects: QuerySet) -> QuerySet:
        children_query = Comment.objects.filter(deleted_at=None)
        return objects.prefetch_related(Prefetch('children', queryset=children_query))
    
    def _select_related_user(self, objects: QuerySet) -> QuerySet:
        return objects.select_related('user')


class ListThread(ServiceWithResult):
    root_id = forms.IntegerField()
    max_depth = forms.IntegerField(required=False, initial=config('THREAD_MAX_DEPTH', int))

    def _read_children_recursively(self, root_id, depth):
        comm = RetrieveComment().execute({"pk": root_id,})
        children = comm.children.all() # only non-deleted children are prefetched
        
        if not children:
            return {comm: []}

        # if max_depth reached, return comm 
        # to create redirect to new view_thread
        # and True, to distinct that there are 
        # still other comments in thread
        if depth >= self.max_depth:
            return {comm: [{comm: True}]}
        
        ancestors = []
        for child in children:
            ancestors.append(self._read_children_recursively(child.id, depth+1))

        return {comm: ancestors}

    def _read_thread(self) -> dict[Comment, list]:
        root_id = self.cleaned_data['root_id']
        self.max_depth = self.cleaned_data['max_depth']
        return self._read_children_recursively(root_id, 0)

    def process(self):
        self.result = self._read_thread()
        return self.result