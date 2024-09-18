import factory
from django.utils.timezone import now

from ...constants import models_const

class PhotoVersionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models_const.get('PhotoVersion')

    title = factory.Faker('sentence', nb_words=7)
    description = factory.Faker('sentence', nb_words=20)
    pub_date = factory.LazyAttribute(lambda self: now())
    path = factory.Faker('file_path')
    status = "Approved"