from drf_spectacular.utils import OpenApiResponse
from service_objects_autodocs.auto_parameters_spectacular import prepare_parameters_for_docs, prepare_request_body_for_docs
from service_objects_autodocs.common import add_pagination_to_data_serializer
from service_objects_autodocs.exceptions import (
    get_authentication_failed_yasg_response,
    get_not_found_error_yasg_response,
    get_validation_error_yasg_response,
    get_yasg_response_with_flat_exception_details,
    get_access_denied_error_yasg_response
)
from api.services.photo import ListPhotos, CreatePhoto, RetrievePhoto, UpdatePhoto, ImportPhoto
from api.serializers.photo import PhotoSerializer

list_photos_docs = {
    "summary": "Get a paginated list of photos",
    "parameters": prepare_parameters_for_docs(
        ListPhotos, exclude=("user",)
    ),
    "responses": {
        "200": OpenApiResponse(
            response=add_pagination_to_data_serializer(PhotoSerializer),
        ),
    },
}

create_photo_docs = {
    "summary": "Create new photo",
    "request": prepare_request_body_for_docs(
        CreatePhoto, exclude=("user",)
    ),
    "responses": {
        "201": OpenApiResponse(response=PhotoSerializer),
        "401": get_authentication_failed_yasg_response(),
    }
}

retrieve_photo_docs = {
    "summary": "Get single photo",
    "parameters": prepare_parameters_for_docs(RetrievePhoto, exclude=("photo_id",)),
    "responses": {
        "200": PhotoSerializer,
        "404": get_not_found_error_yasg_response()
    },
}

update_photo_docs = {
    "summary": "Update photo's information",
    "request": prepare_request_body_for_docs(UpdatePhoto, exclude=("photo",)),
    "responses": {
        "200": PhotoSerializer,
        "400": get_validation_error_yasg_response(),
        "404": get_not_found_error_yasg_response()
    },
}

def get_gone_response(message: str):
    return get_yasg_response_with_flat_exception_details(
        description="Resource is gone",
        exception_type="ResourceDeleted",
        message=message,
        translation_key="gone",
        debug_message="Resource you are asking for is deleted or set to be deleted by owner",
        details=None,
    )

delete_photo_docs = {
    "summary": "Schedule photo's delayed deletion",
    "responses": {
        "202": "",
        "403": get_access_denied_error_yasg_response(details="You are not an owner of this resource"),
        "404": get_not_found_error_yasg_response(),
        "410": get_gone_response(message="Photo alreay set to be deleted")
    }
}

recover_photo_docs = {
    "summary": "Cancel photo deletion",
    "responses": {
        "200": "",
        "403": get_access_denied_error_yasg_response(details="You are not an owner of this resource"),
    }
}

import_photos_docs = {
    "tags": ["photos"],
    "summary": "Import photos from json.",
    "description": """This endpoint accepts list of objects describing photo and it's author to import into DB. 
    **Api key is required to use this endpoint**""",
    "request": prepare_request_body_for_docs(ImportPhoto),
    "responses": {
        "200": "",
        "400": get_validation_error_yasg_response(message="Unable to fetch image. Check URL and it's accessibility"),
        "403": get_access_denied_error_yasg_response(details="Api keys is missing or invalid")
    },
}
