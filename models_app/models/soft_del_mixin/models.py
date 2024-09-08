from django.db import models

class SoftDelMixin(models.Model):
    class Meta:
        abstract = True
    
    deleted_at = models.DateTimeField(null=True, default=None)