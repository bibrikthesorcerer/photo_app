from service_objects.services import ServiceWithResult
from service_objects.errors import ValidationError
from service_objects.fields import ModelField

from models_app.models import ReviewTicket


class SetReviewTicketToSeen(ServiceWithResult):
    ticket = ModelField(ReviewTicket)

    def process(self):
        self.result = self._set_ticket_to_seen()
        return self
    
    def _set_ticket_to_seen(self):
        ticket: ReviewTicket = self.cleaned_data.get("ticket")
        if ticket.is_seen:
            self.add_error("ticket", ValidationError("Given ticket was already seen"))
            self.stop_process()
        ticket.is_seen = True
        ticket.save()
        return ticket