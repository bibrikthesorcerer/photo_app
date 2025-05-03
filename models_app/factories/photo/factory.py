import factory
from django.utils import timezone
from factory import fuzzy, SubFactory, LazyAttribute
from factory.django import ImageField

from models_app.factories.user_profile import UserProfileFactory
from models_app.models import Photo

class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "models_app.Photo"

    user = SubFactory(UserProfileFactory)
    title = fuzzy.FuzzyText(length=64)
    description = fuzzy.FuzzyText(length=256)
    pub_date = fuzzy.FuzzyDateTime(start_dt=timezone.now().replace(year=2024))
    status = fuzzy.FuzzyChoice(
        choices=[x[0] for x in Photo.STATUS_CHOICES],
        getter=lambda c: c[0]
    )
    img = ImageField(
        width=1000,
        height=1000,
        filename='sample.jpg',
        color='blue'
    )

    class Params:
        approved = factory.Trait(
            status=Photo.APPROVED,
            pub_date=LazyAttribute(lambda _: timezone.now() - timezone.timedelta(hours=1))
        )
        to_be_deleted = factory.Trait(
            status=Photo.TO_BE_DELETED,
            pub_date=fuzzy.FuzzyChoice([
                None,
                LazyAttribute(lambda _: timezone.now() - timezone.timedelta(hours=1))
            ])
        )
        on_moderation = factory.Trait(
            status=Photo.ON_MODERATION,
            pub_date=None
        )
        denied = factory.Trait(
            status=Photo.DENIED,
        )

    @factory.post_generation
    def handle_save_signals(self, create, extracted, **kwargs):
        if create and not kwargs.get('skip_signals', True):
            Photo.save_file(Photo, self, created=True)