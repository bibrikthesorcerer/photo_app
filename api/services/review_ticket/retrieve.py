from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound
from django import forms

from models_app.models import ReviewTicket, Photo, PhotoVersion


class RetrieveReviewTicket(ServiceWithResult):
    ticket_id = forms.IntegerField()

    def process(self):
        self.result = self._get_ticket_instance()
        return self
    
    def _get_ticket_manager(self):
        self.objects = ReviewTicket.objects

    def _prefetch_reviewed_object(self):
        self.objects = self.objects.prefetch_related("reviewed_object")

    def _get_ticket_instance(self):
        self._get_ticket_manager()
        self._prefetch_reviewed_object()
        ticket_id = self.cleaned_data.get("ticket_id")
        
        try:
            self.ticket = self.objects.get(id=ticket_id)
        except ReviewTicket.DoesNotExist:
            self.add_error("ticket_id", NotFound(message="Ticket with given id not found"))
            self.stop_process()
        
        self._add_user_to_ticket()
        return self.ticket

    def _add_user_to_ticket(self):
        reviewed_obj = self.ticket.reviewed_object
        if isinstance(reviewed_obj, Photo):
            setattr(self.ticket, 'user', reviewed_obj.user)
        elif isinstance(reviewed_obj, PhotoVersion):
            setattr(self.ticket, 'user', reviewed_obj.photo.user)