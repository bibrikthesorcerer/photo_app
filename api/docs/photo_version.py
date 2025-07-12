from drf_spectacular.utils import OpenApiResponse
from service_objects_autodocs.exceptions import (
    get_not_found_error_yasg_response,
    get_access_denied_error_yasg_response
)
from api.serializers.photo_version import RetrievePhotoVersionSerializer

list_photo_versions_docs = {
    "tags": ["versions"],
    "summary": "Get a list of photo versions for specific photo",
    # "parameters": prepare_parameters_for_docs(
    #     ListPhotoVersions, exclude=("photo",)
    # ),
    "responses": {
        "200": OpenApiResponse(
            response=RetrievePhotoVersionSerializer,
        ),
        "403": get_access_denied_error_yasg_response(details="You are not an owner of this resource"),
        "404": get_not_found_error_yasg_response(),
    },
}