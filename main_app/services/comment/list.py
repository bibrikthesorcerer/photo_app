from service_objects.services import ServiceWithResult
from django import forms
from django.db.models import QuerySet, Prefetch
from decouple import config

from main_app.services.comment import RetrieveComment
from models_app.models import Comment

class ListComments(ServiceWithResult):
    """
    Lists Comment objects or QuerySets with info about users and children comments

    Parameters
    ----------
        include_deleted (bool, optional): whether or not to give out deleted comments
        photo_id (int, optional): id of a photo to which comments are left
        roots_only (bool, optional): whether or not to give out only root comments
    """
    include_deleted = forms.BooleanField(required=False)
    photo_id = forms.IntegerField(required=False)
    roots_only = forms.BooleanField(required=False)
    
    def process(self) -> QuerySet[Comment]:
        objects = self._all_comments_query()
        objects = self._prefetch_children(objects)
        objects = self._select_related_user(objects)
        objects = self._order_by_date(objects)
        objects = self._apply_filters(objects)

        self.result = objects
        return self.result
    
    def _order_by_date(self, objects: QuerySet[Comment]) -> QuerySet[Comment]:
        return objects.order_by('-pub_date')
    
    #@validate_param('include_deleted')
    def _apply_filters(self, objects: QuerySet[Comment]) -> QuerySet[Comment]:
        include_deleted = self.cleaned_data['include_deleted']
        photo_id = self.cleaned_data['photo_id']
        roots_only = self.cleaned_data['roots_only']

        if not include_deleted:
            objects = objects.filter(deleted_at=None)
        if photo_id:
            objects = objects.filter(photo=photo_id)
        if roots_only:
            objects = objects.filter(parent__isnull=True)
        
        return objects
    
    def _all_comments_query(self) -> QuerySet[Comment]:
        return Comment.objects.all()
    
    def _prefetch_children(self, objects: QuerySet[Comment]) -> QuerySet[Comment]:
        children_query = Comment.objects.filter(deleted_at=None)
        return objects.prefetch_related(Prefetch('children', queryset=children_query))
    
    def _select_related_user(self, objects: QuerySet[Comment]) -> QuerySet[Comment]:
        return objects.select_related('user')


class ListThread(ServiceWithResult):
    """
    Lists thread starting from specified root comment and going as deep as max_depth

    Parameters
    ----------
        root_id (int): id of root comment of thread
        max_depth (int, optional): how deep into descendants service should traverse
    """
    root_id = forms.IntegerField()
    max_depth = forms.IntegerField(required=False)

    def process(self) -> tuple[dict[Comment, list[dict]], int]:
        self.result = (self._read_thread(), self.max_depth)
        return self.result

    def _read_children_recursively(self, root_id, depth) -> dict[Comment, list[dict]]:
        comm = RetrieveComment().execute({"pk": root_id,})
        children = comm.children.all() # only non-deleted children are prefetched
        
        if not children:
            return {comm: [{}]}

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

    def _read_thread(self) -> dict[Comment, list[dict]]:
        root_id = self.cleaned_data['root_id']
        self.max_depth = self.cleaned_data['max_depth'] or config('THREAD_MAX_DEPTH', cast=int)
        return self._read_children_recursively(root_id, 0)