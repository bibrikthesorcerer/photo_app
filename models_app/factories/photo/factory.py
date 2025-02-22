import factory
from django.utils.timezone import now


class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "models_app.Photo"

    # user
    # like_set
    # comment_set
    # photoversion_set
    title = factory.Faker("sentence")
    pub_date = factory.LazyAttribute(lambda self: now())
    description = factory.Faker("paragraph")
    path = factory.Faker("file_path")
    status = "Approved"
    created_at = factory.LazyAttribute(lambda _: now())
    updated_at = factory.LazyAttribute(lambda self: now())
