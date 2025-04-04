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
        self.result = self._get_paginated_queryset()
        return self.result

    def _get_photos_manager(self):
        self.objects = Photo.objects
  
    def _get_paginated_queryset(self) -> QuerySet:
        self._get_photos_manager()
        self._add_extra_params()
        per_page = self.cleaned_data.get('per_page') or config('PHOTOS_PER_PAGE', cast=int)
        page = self.cleaned_data.get('page')
        return Paginator(self.objects, per_page).get_page(page)
    
    def _add_extra_params(self):
        self._count_likes_and_comments()
        self._select_related_user()
        self._is_liked_by_user()
        self._apply_filters()
        self._order_data_by()
        self._search_for_entry()
    
    def _build_filters(self) -> Q:
        filters = Q()
        if self.cleaned_data.get('author'):
            filters.add(Q(user=self.cleaned_data.get('author')), Q.AND)
        if self.cleaned_data.get('status'):
            filters.add(Q(status=self.cleaned_data.get('status')), Q.AND)

        return filters

    def _apply_filters(self):        
        self.objects = self.objects.filter(self._build_filters())

    # @validate_param('user')
    def _is_liked_by_user(self):
        user = self.cleaned_data.get('user')
        if not user:
                return
        
        like_subquery = Like.objects.filter(
                photo=OuterRef('pk'),
                user=user,
                deleted_at=None
        )
        
        self.objects = self.objects.annotate(is_liked=Exists(like_subquery))

    # @validate_param('entry')
    def _search_for_entry(self):
        entry = self.cleaned_data.get('entry')
        if not entry:
                return
        
        self.objects = self.objects.filter(
                Q(title__icontains=entry) | 
                Q(description__icontains=entry) | 
                Q(user__username__icontains=entry)
                )

    # @validate_param('order')
    def _order_data_by(self):
        ordering = self.cleaned_data.get('order')
        if not ordering:
                return
        
        self.objects = self.objects.order_by(ordering)

    def _count_likes_and_comments(self):
        self.objects = self.objects.annotate(
                likes_count=Count('like', filter=Q(like__deleted_at=None), distinct=True), 
                comments_count=Count('comment', filter=Q(comment__deleted_at=None), distinct=True))

    def _select_related_user(self):
        self.objects = self.objects.select_related('user')
