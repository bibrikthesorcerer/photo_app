import factory
from django.utils import timezone
from factory import fuzzy, SubFactory

from models_app.factories import PhotoFactory


class PhotoVersionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "models_app.PhotoVersion"

    title = fuzzy.FuzzyText(length=32)
    description = fuzzy.FuzzyText(length=128)
    img = factory.django.ImageField(
        width=1000,
        height=1000,
        filename='sample_version.jpg',
        color='red'
    )
    photo = SubFactory(PhotoFactory)
    iteration = fuzzy.FuzzyInteger(low=1)