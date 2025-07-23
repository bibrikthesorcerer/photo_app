from drf_spectacular.utils import OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from service_objects_autodocs.auto_parameters_spectacular import prepare_request_body_for_docs
from service_objects_autodocs.exceptions import (
    get_authentication_failed_yasg_response,
    get_validation_error_yasg_response
)
from api.serializers.user_profile import UserProfileSerializer
from api.services.user_profile import UpdateUserProfile, CreateUserProfile, AuthenticateUserAndRenewApiToken

get_current_user_docs = {
    "tags": ["current user"],
    "summary": "Retrieve current user's info",
    "responses": {
        "200": OpenApiResponse(
            response=UserProfileSerializer,
        ),
        "401": get_authentication_failed_yasg_response(),
    },
}

update_current_user_docs = {
    "tags": ["current user"],
    "summary": "Update current user's info",
    "request": prepare_request_body_for_docs(UpdateUserProfile, exclude=("user",)),
    "responses": {
        "200": OpenApiResponse(
            response=UserProfileSerializer,
        ),
        "401": get_authentication_failed_yasg_response(),
    },
}

create_new_user_docs = {
    "summary": "Register new user profile and get new user's Api token as a result",
    "request": prepare_request_body_for_docs(CreateUserProfile),
    "responses": {
        "200": OpenApiTypes.STR,
        "400": get_validation_error_yasg_response(),
    },
}

renew_token_docs = {
    "summary": "Check user credentials and return fresh Api token for given user",
    "request": prepare_request_body_for_docs(AuthenticateUserAndRenewApiToken),
    "responses": {
        "200": OpenApiTypes.STR,
        "400": get_validation_error_yasg_response(),
    },
}

forget_tokens_docs = {
    "summary": "Logout user, reject all tokens issued before this logout",
    "responses": {
        "200": {},
        "401": get_authentication_failed_yasg_response(),
    },
}