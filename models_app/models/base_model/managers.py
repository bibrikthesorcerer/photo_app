from django.db import models
from django.utils.timezone import now

class SoftDelQuerySet(models.QuerySet):
    def delete(self):
        deleted_ts = now()
        self.update(deleted_at=deleted_ts)
        return self

class SoftDelManager(models.Manager):
    def get_queryset(self):
        return SoftDelQuerySet(self.model)