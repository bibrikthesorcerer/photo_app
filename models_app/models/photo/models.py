from django.db import models
from ..meta_abstract.models import MetaAbstract

class Photo(MetaAbstract):
    # like_set
    # comment_set
    # photoversion_set
    user = models.ForeignKey('models_app.UserProfile', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    pub_date = models.DateTimeField()
    path = models.CharField(max_length=256)
    status = models.CharField(max_length=16)

    def __str__(self):
        return f'{self.title}'