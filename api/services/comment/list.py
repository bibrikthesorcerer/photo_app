from service_objects.services import ServiceWithResult
from django import forms
from decouple import config
from django.db.models import Q
from django.core.paginator import Paginator, Page

from models_app.models import Comment

class ListComments(ServiceWithResult):
    ORDER_CHOICES = (
        ("pub_date", "", ),
        ("-pub_date", "", ),
    )
    photo_id = forms.IntegerField(required=False)
    roots_only = forms.BooleanField(required=False)
    page = forms.IntegerField(required=False)
    per_page = forms.IntegerField(required=False)
    order = forms.ChoiceField(choices=ORDER_CHOICES, initial="-pub_date", required=False)
    id = forms.IntegerField(required=False)

    def process(self) -> Page:
        self.result = self._get_paginated_queryset()
        return self.result
    
    def _get_paginated_queryset(self) -> Page:
        self._get_comments_manager()
        self._add_extra_params()
        return self._paginate_queryset()
    
    def _paginate_queryset(self) -> Page:
        per_page = self.cleaned_data.get('per_page') or config('COMMENTS_PER_PAGE', default=20, cast=int)
        page = self.cleaned_data.get('page')
        return Paginator(self.objects, per_page).get_page(page)
    
    def _get_comments_manager(self):
        self.objects = Comment.objects

    def _add_extra_params(self):
        self._select_related()
        self._order_objects()
        self._apply_filters()

    def _select_related(self):
        self.objects = self.objects.select_related('user')

    def _build_filters(self) -> Q:
        filters = Q()
        if self.cleaned_data.get("photo_id"):
            filters.add(Q(photo=self.cleaned_data.get("photo_id")), Q.AND)
        if self.cleaned_data.get("roots_only"):
            filters.add(Q(parent__isnull=True), Q.AND)
        if self.cleaned_data.get("id"):
            filters.add(Q(id__in=self._get_thread_ids(self.cleaned_data.get("id"))), Q.AND)

        # filter deleted comments
        filters.add((
            Q(deleted_at=None) 
            | (Q(text__exact="DELETED")&~Q(deleted_at=None))
        ),Q.AND)

        return filters
    
    def _apply_filters(self):
        self.objects = self.objects.filter(self._build_filters())

    def _order_objects(self):
        order = self.cleaned_data.get("order") or self.fields["order"].initial
        self.objects = self.objects.order_by(order)

    def _get_thread_ids(self, root_id):
        thread_ids = [root_id]
        thread_ids.extend(self._traverse_children_recursively(root_id))
        return thread_ids
    
    def _traverse_children_recursively(self, root_id):
        children_ids = list(Comment.objects.filter(parent=root_id).values_list("id", flat=True))
        descendants_ids = []
        for id in children_ids:
            # get all children of specific child
            descendants_ids.extend(self._get_thread_ids(id))
        children_ids.extend(descendants_ids)
        return children_ids