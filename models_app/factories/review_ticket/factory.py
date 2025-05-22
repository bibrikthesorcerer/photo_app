import factory
from django.contrib.contenttypes.models import ContentType
import factory.fuzzy

from models_app.factories import UserProfileFactory
from models_app.models import Photo, PhotoVersion, ReviewTicket


class ReviewTicketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "models_app.ReviewTicket"

    moderator = factory.SubFactory(UserProfileFactory)
    commentary = factory.fuzzy.FuzzyText()
    result = factory.fuzzy.FuzzyChoice(
        choices=[x[0] for x in ReviewTicket.REVIEW_RESULT_CHOICES],
        getter=lambda c: c[0]
    )
    content_type = factory.LazyAttribute(
        lambda self: ContentType.objects.get_for_model(self.reviewed_object)
    )
    object_id = factory.LazyAttribute(
        lambda self: self.reviewed_object.id
    )

    class Params:
        reviewed_object = None