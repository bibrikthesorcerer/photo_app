import factory
from django.utils.timezone import now


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "models_app.Comment"

    # user
    # photo
    # parent
    # children
    text = factory.Faker("sentence", nb_words=5)
    pub_date = factory.LazyAttribute(lambda self: now())
    deleted_at = None
