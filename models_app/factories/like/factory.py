import factory
from models_app.factories.user_profile import UserProfileFactory
from models_app.factories.photo import PhotoFactory


class LikeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "models_app.Like"

    user = factory.SubFactory(UserProfileFactory)
    photo = factory.SubFactory(PhotoFactory)
    deleted_at = None
