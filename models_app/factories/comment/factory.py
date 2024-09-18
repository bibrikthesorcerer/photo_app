import factory
from django.utils.timezone import now

from ...constants import models_const

class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models_const.get('Comment')

    # user
    # photo
    # parent
    # children
    text = factory.Faker('sentence', nb_words=5)
    pub_date = factory.LazyAttribute(lambda self: now())
    deleted_at = None