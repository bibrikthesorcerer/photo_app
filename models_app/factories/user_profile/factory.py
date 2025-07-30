import factory
from django.utils import timezone
from factory import fuzzy

from models_app.models import UserProfile


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "models_app.UserProfile"
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    date_joined = fuzzy.FuzzyDateTime(start_dt=timezone.now().replace(year=2024))
    role = fuzzy.FuzzyChoice(
        [UserProfile.ROLE_USER, UserProfile.ROLE_MOD, UserProfile.ROLE_ADMIN]
    )
    password = factory.PostGenerationMethodCall("set_password", "testpass123")

    class Params:
        admin = factory.Trait(
            role=UserProfile.ROLE_ADMIN, is_staff=True, is_superuser=True
        )
        moderator = factory.Trait(role=UserProfile.ROLE_MOD, is_staff=True)
        user = factory.Trait(
            role=UserProfile.ROLE_USER, is_staff=False, is_superuser=False
        )
