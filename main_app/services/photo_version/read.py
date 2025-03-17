from service_objects.services import ServiceWithResult
from models_app.models import PhotoVersion
from django.db.models import QuerySet, Q
from django import forms

class ReadPhotoVersionsByPhotoID(ServiceWithResult):
    """
    Lists photo versions associated with photo, orders them by iteration number and prefetches Reviews
    Parameters
    ----------
        photo_id (int): id of a associated photo
    """
    photo_id = forms.IntegerField()

    def process(self) -> QuerySet[PhotoVersion]:
        self.result = self._get_photo_versions()
        return self.result
    
    def _get_photo_versions(self):
        self._get_all_versions()
        self._apply_filters()
        self._prefetch_related()
        self._order()
        return self.objects

    def _get_all_versions(self):
        self.objects = PhotoVersion.objects

    def _build_filters(self):
        filters = Q()
        filters.add(Q(photo=self.cleaned_data.get('photo_id')), Q.AND)
        return filters
        
    def _apply_filters(self):
        self.objects = self.objects.filter(self._build_filters())

    def _prefetch_related(self):
        self.objects = self.objects.prefetch_related('review_tickets')
    
    def _order(self):
        self.objects = self.objects.order_by('-iteration')