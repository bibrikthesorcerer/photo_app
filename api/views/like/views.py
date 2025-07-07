from service_objects.services import ServiceOutcome
from rest_framework.response import Response
from rest_framework import status

from api.views import BaseView
from api.permissions import IsOwner, PlainUserOnly
from api.services import UpdateOrCreateLike, DeleteLike, RetrieveLike
from api.serializers import RetrieveLikeSerializer


class LikesView(BaseView):
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [PlainUserOnly]
        if self.request.method == 'DELETE':
            self.permission_classes = [IsOwner]
        return super().get_permissions()

    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            UpdateOrCreateLike,
            ({"user": request.user} | kwargs)
        )
        data = RetrieveLikeSerializer(outcome.result).data
        return Response(data, status=status.HTTP_201_CREATED)
    
    def _get_like_with_permission_check(self):
        outcome = ServiceOutcome(RetrieveLike, ({"user_id": self.request.user.id} | self.kwargs))
        like = outcome.result
        self.check_object_permissions(self.request, like)
        return like

    def delete(self, request, *args, **kwargs):
        self._get_like_with_permission_check()
        outcome = ServiceOutcome(
            DeleteLike,
            ({"user_id": request.user.id} | kwargs)
        )
        data = RetrieveLikeSerializer(outcome.result).data
        return Response(status=status.HTTP_200_OK)