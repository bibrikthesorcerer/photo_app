import factory
from django.utils.timezone import now

from ...constants import models_const

class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'models_app.UserProfile')

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    date_joined = factory.LazyAttribute(lambda _: now())
    password = factory.Faker('sha256')