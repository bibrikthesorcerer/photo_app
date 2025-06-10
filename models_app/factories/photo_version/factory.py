import factory
from django.utils import timezone
from factory import fuzzy, SubFactory

from models_app.factories import PhotoFactory


class PhotoVersionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "models_app.PhotoVersion"

    title = factory.Faker("sentence", nb_words=7)
    description = factory.Faker("sentence", nb_words=20)
    img = factory.django.ImageField(
        width=1000,
        height=1000,
        filename='sample_version.jpg',
        color='red'
    )
    photo = SubFactory(PhotoFactory)
    iteration = fuzzy.FuzzyInteger(low=1)