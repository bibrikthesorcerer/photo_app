from drf_spectacular.utils import OpenApiResponse
from service_objects_autodocs.exceptions import (
    get_not_found_error_yasg_response,
    get_access_denied_error_yasg_response
)
from api.serializers.review_ticket import RetrieveReviewTicketSerializer

set_ticket_to_seen_docs = {
    "summary": "Set review ticket to seen",
    "responses": {
        "200": OpenApiResponse(
            response=RetrieveReviewTicketSerializer,
        ),
        "403": get_access_denied_error_yasg_response(details="You are not an owner of this resource"),
        "404": get_not_found_error_yasg_response(),
    },
}