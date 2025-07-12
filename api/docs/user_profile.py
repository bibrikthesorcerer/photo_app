from drf_spectacular.utils import OpenApiResponse
from service_objects_autodocs.auto_parameters_spectacular import prepare_request_body_for_docs
from service_objects_autodocs.exceptions import (
    get_authentication_failed_yasg_response,
    get_access_denied_error_yasg_response
)
from api.serializers.user_profile import UserProfileSerializer
from api.services.user_profile import UpdateUserProfile

get_current_user_docs = {
    "summary": "Retrieve current user's info",
    "responses": {
        "200": OpenApiResponse(
            response=UserProfileSerializer,
        ),
        "401": get_authentication_failed_yasg_response(),
    },
}

update_current_user_docs = {
    "summary": "Update current user's info",
    "request": prepare_request_body_for_docs(UpdateUserProfile, exclude=("user",)),
    "responses": {
        "200": OpenApiResponse(
            response=UserProfileSerializer,
        ),
        "401": get_authentication_failed_yasg_response(),
    },
}