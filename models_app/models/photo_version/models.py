from django.db import models

from ..meta_abstract.models import MetaAbstract

class PhotoVersion(MetaAbstract):
    photo = models.ForeignKey('models_app.Photo', on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    pub_date = models.DateTimeField(null=True, default=None, blank=True)
    status = models.CharField(max_length=16)
    img = models.ImageField()

    def __str__(self):
        return f"{self.photo.title} - version"