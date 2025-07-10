from rest_framework import status
from rest_framework.response import Response
from service_objects.services import ServiceOutcome

from api.views import BaseView
from api.permissions import IsOwner
from api.serializers import RetrieveReviewTicketSerializer
from api.services import RetrieveReviewTicket, SetReviewTicketToSeen


class ReviewTicketView(BaseView):
    permission_classes = [IsOwner]

    def patch(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            SetReviewTicketToSeen,
            {"ticket": self._get_object_with_permission_check(RetrieveReviewTicket)}
        )
        data = RetrieveReviewTicketSerializer(outcome.result).data
        return Response(data, status=status.HTTP_200_OK)