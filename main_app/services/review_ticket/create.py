from django import forms
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from django.contrib.contenttypes.models import ContentType

from models_app.models import ReviewTicket, UserProfile, Photo

class CreateReviewTicket(ServiceWithResult):
    """
    Creates ReviewTicket based on photo id

    Parameters
    ----------
        object_id (int): id of a photo being reviewed
        moderator (UserProfile)
        commentary (str)
        result (str, choice): review result - Approved/Denied
    """
    object_id = forms.IntegerField()
    moderator = ModelField(UserProfile)
    commentary = forms.CharField(required=False)
    result = forms.ChoiceField(choices=ReviewTicket.REVIEW_RESULT_CHOICES)

    def process(self):
        self.result = ReviewTicket.objects.create(
            **(self.cleaned_data
               | {"content_type": ContentType.objects.get_for_model(Photo)})
        )
        return self.result