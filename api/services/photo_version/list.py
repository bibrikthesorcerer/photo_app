from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from django import forms
from django.db.models import Q

from models_app.models import PhotoVersion, Photo


class ListPhotoVersions(ServiceWithResult):
    photo = ModelField(Photo)

    def process(self):
        self.result = self._get_photo_versions()
        return self
    
    def _get_photo_versions(self):
        self._get_versions_manager()
        self._prefetch_related()
        self._apply_filters()
        return self.objects
    
    def _get_versions_manager(self):
        self.objects = PhotoVersion.objects

    def _prefetch_related(self):
        self.objects = self.objects.prefetch_related("review_tickets")

    def _apply_filters(self):
        self.objects = self.objects.filter(self._build_filters())

    def _build_filters(self):
        filters = Q()
        photo = self.cleaned_data.get("photo")
        filters.add(Q(photo_id=photo.id), Q.AND)
        return filters