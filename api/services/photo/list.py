from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from django import forms
from django.db.models import OuterRef, Q, Exists, Count
from decouple import config
from django.core.paginator import Paginator, Page

from models_app.models import Photo, UserProfile, Like


class ListPhotos(ServiceWithResult):
    entry = forms.CharField(required=False, help_text="String for searching through photos. Search happens in title, description and author name.")
    user = ModelField(UserProfile, required=False)
    author_id = forms.IntegerField(required=False, help_text="Filter photos by author.")
    per_page = forms.IntegerField(required=False)
    page = forms.IntegerField(required=False)
    status = forms.ChoiceField(
        choices=Photo.STATUS_CHOICES,
        required=False,
        help_text=""
    )

    ORDER_CHOICES = (
        ("likes_count", "", ),
        ("-likes_count", "", ),
        ("pub_date", "", ),
        ("-pub_date", "", ),
        ("comments_count", "", ),
        ("-comments_count", "", ),
    )
    order = forms.ChoiceField(choices=ORDER_CHOICES, required=False) 

    def process(self) -> Page:
        self.result = self._get_paginated_queryset()
        return self

    def _get_photos_manager(self):
        self.objects = Photo.objects
  
    def _get_paginated_queryset(self) -> Page:
        self._get_photos_manager()
        self._add_extra_params()
        per_page = self.cleaned_data.get('per_page') or config('PHOTOS_PER_PAGE', default=20, cast=int)
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
        if self.cleaned_data.get('author_id'):
            filters.add(Q(user=self.cleaned_data.get('author_id')), Q.AND)
        if self.cleaned_data.get('status'):
            filters.add(Q(status=self.cleaned_data.get('status')), Q.AND)

        return filters

    def _apply_filters(self):        
        self.objects = self.objects.filter(self._build_filters())

    def _is_liked_by_user(self):
        user = self.cleaned_data.get('user')
        if user:
            like_subquery = Like.objects.filter(
                    photo=OuterRef('pk'),
                    user=user,
                    deleted_at=None
            )
            self.objects = self.objects.annotate(is_liked=Exists(like_subquery))

    def _search_for_entry(self):
        entry = self.cleaned_data.get('entry')
        if entry:
            self.objects = self.objects.filter(
                    Q(title__icontains=entry) 
                    | Q(description__icontains=entry) 
                    | Q(user__username__icontains=entry)
            )

    def _order_data_by(self):
        order = self.cleaned_data.get('order')
        if order:
            self.objects = self.objects.order_by(order)

    def _count_likes_and_comments(self):
        self.objects = self.objects.annotate(
                likes_count=Count('like', filter=Q(like__deleted_at=None), distinct=True), 
                comments_count=Count('comment', filter=Q(comment__deleted_at=None), distinct=True))

    def _select_related_user(self):
        self.objects = self.objects.select_related('user')

