from django.db import models
from ..meta_abstract.models import MetaAbstract
from ..soft_del_mixin.models import SoftDelMixin
from ...constants import models_const

class Like(MetaAbstract, SoftDelMixin):
    photo = models.ForeignKey(models_const.get('Photo'), on_delete=models.CASCADE)
    user = models.ForeignKey(models_const.get('UserProfile'), on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} on {self.photo}'