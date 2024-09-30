from django.db import models
from ..meta_abstract.models import MetaAbstract
from ..soft_del_mixin.models import SoftDelMixin

class Comment(MetaAbstract, SoftDelMixin):
    user = models.ForeignKey('models_app.UserProfile', on_delete=models.CASCADE)
    photo = models.ForeignKey('models_app.Photo', on_delete=models.CASCADE)
    text = models.CharField(max_length=256)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, related_name='children',null=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.text}'