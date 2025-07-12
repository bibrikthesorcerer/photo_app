from drf_spectacular.utils import OpenApiResponse
from service_objects_autodocs.exceptions import (
    get_authentication_failed_yasg_response,
    get_not_found_error_yasg_response,
    get_access_denied_error_yasg_response,
)

from api.services.like import UpdateOrCreateLike, DeleteLike
from api.serializers.like import RetrieveLikeSerializer

create_like_docs = {
    "tags": ["like"],
    "summary": "Leave a like under a photo",
    # "parameters": prepare_parameters_for_docs(UpdateOrCreateLike, exclude=("user")),
    "responses": {
        "201": OpenApiResponse(response=RetrieveLikeSerializer),
    },
}

delete_like_docs = {
    "tags": ["like"],
    "summary": "Delete like under a photo using soft deletion",
    "description": """Uses *soft deletion* to delete like under a photo, i.e. sets special `deleted_at` field to time of deletion.
    **This will also trigger WebSocket notification for the author of the photo.**""",
    # "parameters": prepare_parameters_for_docs(DeleteLike, exclude=("user")),
    "responses": {
        "200": OpenApiResponse(response=RetrieveLikeSerializer),
        "401": get_authentication_failed_yasg_response(),
        "403": get_access_denied_error_yasg_response(details="You are not an owner of this resource"),
        "404": get_not_found_error_yasg_response()
    },
}