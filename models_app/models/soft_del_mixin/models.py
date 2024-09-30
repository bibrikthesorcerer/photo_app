from django.db import models

class SoftDelMixin(models.Model):
    deleted_at = models.DateTimeField(null=True, default=None, blank=True)
    
    class Meta:
        abstract = True
    