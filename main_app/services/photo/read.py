from service_objects.services import ServiceWithResult
from service_objects.fields import DictField, ModelField
from django.db.models import Count, QuerySet, Exists, OuterRef
from django import forms
from django.db.models import Q
from django.core.paginator import Paginator

from models_app.models import Photo, Like, UserProfile

class ReadPhotos(ServiceWithResult):
      """
      Retrieves Photo objects or QuerySets with info about users, number of likes and comments

      Parameters
      ----------
            filter (dict): filter parameters (e.g. pk=1)
            order (str): name of a field from given choices. may be prefixed with a minus sign (e.g. -likes_count)
            entry (str): string used to filter objects which contains given entry
            first (bool): return first result
            user (UserProfile): a user who is requesting list of photos. used to calculate is_liked field
            pk (int): return only one object with given Primary Key, ignoring filters/entries/order/pagination
            per_page (int): how many objects per page should paginator group. 20 by default
      """
      filter = DictField(required=False)
      entry = forms.CharField(required=False)
      first = forms.BooleanField(required=False)
      user = ModelField(UserProfile, required=False)
      pk = forms.IntegerField(required=False)
      per_page = forms.IntegerField(required=False)

      ORDER_CHOICES = (
            ("likes_count", "", ),
            ("-likes_count", "", ),
            ("pub_date", "", ),
            ("-pub_date", "", ),
            ("comments_count", "", ),
            ("-comments_count", "", ),
      )
      order = forms.ChoiceField(choices=ORDER_CHOICES, required=False)

      def process(self):
            objects = self._read_all_data()
            objects = self._count_likes_and_comments(objects)
            objects = self._select_related_user(objects)
            
            user = self.cleaned_data['user']
            if user:
                  objects = self._is_liked_by_user(objects, user)
            
            pk = self.cleaned_data['pk']
            if pk:
                  return self._get_object(objects, pk)
                        
            filters = self.cleaned_data['filter']
            if filters:
                  objects = self._filter_data(objects, filters)
            
            ordering = self.cleaned_data['order']
            if ordering:
                  objects = self._order_data_by(objects, ordering)

            entry = self.cleaned_data['entry']
            if entry:
                  objects = self._filter_data_by_entry(objects, entry)
            
            if self.cleaned_data['first']:
                  objects = self._first_object(objects)
            else:
                  objects = self._get_paginated_queryset(objects)
            
            self.result = objects
            return self.result

      def _read_all_data(self):
            return Photo.objects.all()
      
      def _get_object(self, objects: QuerySet, pk: int) -> QuerySet:
            return objects.get(pk=pk)
      
      def _get_paginated_queryset(self, objects: QuerySet) -> QuerySet:
            per_page = self.cleaned_data['per_page'] or 20
            return Paginator(objects, per_page)

      def _filter_data(self, objects: QuerySet, filters: dict) -> QuerySet:
            return objects.filter(**filters)
      
      def _is_liked_by_user(self, objects: QuerySet, user: UserProfile) -> QuerySet:
            like_subquery = Like.objects.filter(
                  photo=OuterRef('pk'),
                  user=user,
                  deleted_at=None
            )
            
            return objects.annotate(is_liked=Exists(like_subquery))
      
      def _filter_data_by_entry(self, objects: QuerySet, entry: str) -> QuerySet:
            return objects.filter(
                  Q(title__icontains=entry) | 
                  Q(description__icontains=entry) | 
                  Q(user__username__icontains=entry)
                  )

      def _order_data_by(self, objects: QuerySet, ordering: str) -> QuerySet:
            return objects.order_by(ordering)
      
      def _first_object(self, objects: QuerySet) -> QuerySet:
            return objects.first()
      
      def _count_likes_and_comments(self, objects: QuerySet) -> QuerySet:
            return objects.annotate(
                  likes_count=Count('like', filter=Q(like__deleted_at=None), distinct=True), 
                  comments_count=Count('comment', filter=Q(comment__deleted_at=None), distinct=True))
      
      def _select_related_user(self, objects: QuerySet) -> QuerySet:
            return objects.select_related('user')
