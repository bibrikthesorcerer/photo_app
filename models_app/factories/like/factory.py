import factory

from ...constants import models_const

class LikeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models_const.get('Like')
    
    # user
    # photo
    deleted_at = None