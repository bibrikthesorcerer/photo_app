from django import forms
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from django.contrib.contenttypes.models import ContentType

from models_app.models import PhotoVersion, ReviewTicket

class UpdateReviewTicketWithVersion(ServiceWithResult):
    """
    Updates ReviewTicket when photo is being archived

    Parameters
    ----------
        photo_id (int): id of photo being archived
        photo_version_id (int): id of PhotoVersion object representing versioned photo
    """
    photo_id = forms.IntegerField()
    photo_version_id = forms.IntegerField()

    def process(self):
        photo_id = self.cleaned_data.get('photo_id')
        photo_version_id = self.cleaned_data.get('photo_version_id')
        ticket = ReviewTicket.objects.get(object_id=photo_id)
        ticket.object_id = photo_version_id
        ticket.content_type = ContentType.objects.get_for_model(PhotoVersion)
        ticket.save(update_fields=['object_id', 'content_type'])
        self.result = ticket
        return self.result