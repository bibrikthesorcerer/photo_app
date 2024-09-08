from django.db import models
from ..meta_abstract.models import MetaAbstract
from ...constants import models_const

class PhotoVersion(MetaAbstract):
    photo = models.ForeignKey(models_const.get('Photo'), on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    pub_date = models.DateTimeField(auto_now=True)
    path = models.CharField(max_length=256)
    status = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.photo.title} - version"