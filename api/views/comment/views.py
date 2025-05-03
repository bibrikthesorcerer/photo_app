from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from service_objects.services import ServiceOutcome, ServiceObjectLogicError
from service_objects.errors import InvalidInputsError

from api.views import BaseView
from api.services import ListComments, CreateComment
from api.serializers import PageSerializer, CommentSerializer

import logging
logger = logging.getLogger()


class CommentsView(BaseView):

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get(self, request):
        comments_query = ListComments.execute({**request.query_params.dict()})
        data = PageSerializer(
            instance=comments_query,
            objects_serializer=CommentSerializer
        ).data
        return Response(data)
    
    def post(self, request):
        try:
            outcome = ServiceOutcome(
                CreateComment,
                (self.request.data | {'user': request.user})
            )
            new_comment = outcome.result
            data = CommentSerializer(new_comment).data
            return Response(data, status=status.HTTP_201_CREATED)
        
        except ServiceObjectLogicError as e:
            return Response(
                {'errors': e.errors_dict, 'info': e.additional_info},
                status=e.response_status
            )
        except InvalidInputsError as e:
            return Response(
                # e.errors.as_data() | e.non_field_errors.as_data(), TODO
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)