from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from service_objects.services import ServiceOutcome, ServiceObjectLogicError
from service_objects.errors import InvalidInputsError
from rest_framework.exceptions import APIException
from rest_framework.decorators import permission_classes

from api.views import BaseView
from api.permissions import IsOwner
from api.services import ListComments, CreateComment, RetrieveComment, UpdateCommentText, DeleteComment
from api.serializers import PageSerializer, CommentSerializer, RetrieveCommentSerializer


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
        outcome = ServiceOutcome(
            CreateComment,
            (self.request.data | {'user': request.user})
        )
        new_comment = outcome.result
        data = CommentSerializer(new_comment).data
        return Response(data, status=status.HTTP_201_CREATED)
        

class SingleCommentView(BaseView):

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            self.permission_classes = [IsOwner]
        return super().get_permissions()
    
    def get_comment_with_permission_check(self):
        outcome = ServiceOutcome(RetrieveComment, self.kwargs)
        comment = outcome.result
        self.check_object_permissions(self.request, comment)
        return comment

    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(RetrieveComment, kwargs)
        comment_obj = outcome.result
        data = RetrieveCommentSerializer(comment_obj).data
        return Response(data)
        
    def put(self, request, *args, **kwargs):
        comment = self.get_comment_with_permission_check()
        update_outcome = ServiceOutcome(
            UpdateCommentText,
            {"comment": comment}|request.data
        )
        data = RetrieveCommentSerializer(update_outcome.result).data
        return Response(data)
        
    def delete(self, request, *args, **kwargs):
        comment = self.get_comment_with_permission_check()
        outcome = ServiceOutcome(DeleteComment, {'comment': comment})
        comment, is_deleted = outcome.result
        data = RetrieveCommentSerializer(comment).data
        data.update({"is_deleted": is_deleted})
        return Response(data, status=status.HTTP_200_OK)