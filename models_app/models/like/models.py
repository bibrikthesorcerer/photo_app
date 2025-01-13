from django.db import models
from ..meta_abstract.models import MetaAbstract
from ..soft_del_mixin.models import SoftDelMixin

class Like(MetaAbstract, SoftDelMixin):
    photo = models.ForeignKey('models_app.Photo', on_delete=models.CASCADE)
    user = models.ForeignKey('models_app.UserProfile', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} on {self.photo}'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['photo','user'], name='unique_photo_user')
        ]