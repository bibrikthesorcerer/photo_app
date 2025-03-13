from typing import Any
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from django.db.models import Count, QuerySet, Exists, OuterRef
from django import forms
from django.db.models import Q
from django.core.paginator import Paginator
from decouple import config

from models_app.models import Photo, Like, UserProfile
from main_app.utils import validate_param

class ListPhotos(ServiceWithResult):
    """
    Returns QuerySets of Photo with info about users, number of likes and comments

    Parameters
    ----------
        order (str, optional): name of a field from given choices. may be prefixed with a minus sign (e.g. -likes_count)
        entry (str, optional): string used to filter objects which contains given entry
        user (UserProfile, optional): a user who is requesting list of photos. used to calculate is_liked field
        author (UserProfile, optional): used to filter photos by user who created them
        per_page (int, optional): how many objects per page should paginator group together
        page (int, optional): number of page that paginator gives out
        status (str, optional): status filter based on Photo's STATUS_CHOICES
    """
    entry = forms.CharField(required=False)
    user = ModelField(UserProfile, required=False)
    author = ModelField(UserProfile, required=False)
    per_page = forms.IntegerField(required=False)
    page = forms.IntegerField(required=False)
    status = forms.ChoiceField(choices=Photo.STATUS_CHOICES, required=False)

    ORDER_CHOICES = (
        ("likes_count", "", ),
        ("-likes_count", "", ),
        ("pub_date", "", ),
        ("-pub_date", "", ),
        ("comments_count", "", ),
        ("-comments_count", "", ),
    )
    order = forms.ChoiceField(choices=ORDER_CHOICES, required=False)

    def process(self) -> QuerySet:
        objects = self._all_photos_query()
        objects = self._count_likes_and_comments(objects)
        objects = self._select_related_user(objects)
        objects = self._is_liked_by_user(objects)                
        objects = self._apply_filters(objects)
        objects = self._order_data_by(objects)
        objects = self._search_for_entry(objects)
        objects = self._get_paginated_queryset(objects)
        
        self.result = objects
        return self.result

    def _all_photos_query(self):
        return Photo.objects.all()
  
    def _get_paginated_queryset(self, objects: QuerySet) -> QuerySet:
        per_page = self.cleaned_data.get('per_page') or config('PHOTOS_PER_PAGE', cast=int)
        page = self.cleaned_data.get('page')
        return Paginator(objects, per_page).get_page(page)
    
    def _build_filters(self) -> Q:
        filters = Q()
        if self.cleaned_data.get('author'):
            filters.add(Q(user=self.cleaned_data.get('author')), Q.AND)
        if self.cleaned_data.get('status'):
            filters.add(Q(status=self.cleaned_data.get('status')), Q.AND)

        return filters

    def _apply_filters(self, objects: QuerySet) -> QuerySet:        
        return objects.filter(self._build_filters())

    @validate_param('user')
    def _is_liked_by_user(self, objects: QuerySet, user) -> QuerySet:
        # user = self.cleaned_data.get('user')
        # if not user:
        #         return objects
        
        like_subquery = Like.objects.filter(
                photo=OuterRef('pk'),
                user=user,
                deleted_at=None
        )
        
        return objects.annotate(is_liked=Exists(like_subquery))

    @validate_param('entry')
    def _search_for_entry(self, objects: QuerySet, entry) -> QuerySet:
        # entry = self.cleaned_data.get('entry')
        # if not entry:
        #         return objects
        
        return objects.filter(
                Q(title__icontains=entry) | 
                Q(description__icontains=entry) | 
                Q(user__username__icontains=entry)
                )

    @validate_param('order')
    def _order_data_by(self, objects: QuerySet, ordering) -> QuerySet:
        # ordering = self.cleaned_data.get('order')
        # if not ordering:
        #         return objects
        
        return objects.order_by(ordering)

    def _first_object(self, objects: QuerySet) -> QuerySet:
        return objects.first()

    def _count_likes_and_comments(self, objects: QuerySet) -> QuerySet:
        return objects.annotate(
                likes_count=Count('like', filter=Q(like__deleted_at=None), distinct=True), 
                comments_count=Count('comment', filter=Q(comment__deleted_at=None), distinct=True))

    def _select_related_user(self, objects: QuerySet) -> QuerySet:
        return objects.select_related('user')
