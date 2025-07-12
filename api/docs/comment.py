from drf_spectacular.utils import OpenApiResponse
from service_objects_autodocs.auto_parameters_spectacular import prepare_parameters_for_docs, prepare_request_body_for_docs
from service_objects_autodocs.common import add_pagination_to_data_serializer
from service_objects_autodocs.exceptions import (
    get_authentication_failed_yasg_response,
    get_validation_error_yasg_response,
    get_not_found_error_yasg_response,
)
from api.services.comment import ListComments, CreateComment, UpdateCommentText, DeleteComment
from api.serializers.comment import CommentSerializer, RetrieveCommentSerializer

list_comments_docs = {
    "summary": "Get a paginated list of comments",
    "parameters": prepare_parameters_for_docs(
        ListComments
    ),
    "responses": {
        "200": OpenApiResponse(
            response=add_pagination_to_data_serializer(CommentSerializer),
        ),
    },
}

create_comment_docs = {
    "summary": "Create new comment under a photo",
    "description": "Leave a comment under photo. **Triggers WebSocket notification for photo's author.**",
    "request": prepare_request_body_for_docs(
        CreateComment, exclude=("user",)
    ),
    "responses": {
        "201": OpenApiResponse(response=CommentSerializer),
        "400": get_validation_error_yasg_response(),
        "401": get_authentication_failed_yasg_response(),
    }
}

retrieve_comment_docs = {
    "summary": "Retrieve single comment",
    # "parameters": prepare_parameters_for_docs(
    #     RetrieveComment
    # ),
    "responses": {
        "200": OpenApiResponse(response=RetrieveCommentSerializer),
        "404": get_not_found_error_yasg_response(),
    }
}

update_comment_docs = {
    "summary": "Edit comment's text",
    # "parameters": prepare_parameters_for_docs(RetrieveComment),
    "request": prepare_request_body_for_docs(UpdateCommentText, exclude=("comment",)),
    "responses": {
        "200": OpenApiResponse(response=RetrieveCommentSerializer),
        "404": get_not_found_error_yasg_response(),
    }
}

delete_comment_docs = {
    "summary": "Delete comment using soft deletion",
    "description": """Uses *soft deletion* to delete comment, i.e. sets special `deleted_at` field to time of deletion.
    If comment have children, will set text to `DELETED` so frontend can display deleted comments with children.""",
    # "parameters": prepare_parameters_for_docs(RetrieveComment),
    "request": prepare_request_body_for_docs(DeleteComment, exclude=("comment",)),
    "responses": {
        "200": OpenApiResponse(response=RetrieveCommentSerializer),
        "404": get_not_found_error_yasg_response(),
    }
}

