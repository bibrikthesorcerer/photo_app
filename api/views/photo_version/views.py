from service_objects.services import ServiceOutcome
from rest_framework.response import Response
from rest_framework import status

from api.views import BaseView
from api.permissions import IsOwner
from api.services import ListPhotoVersions, RetrievePhoto
from api.serializers import RetrievePhotoVersionSerializer


class PhotoVersionView(BaseView):
    permission_classes = [IsOwner]

    def _get_photo_with_permission_check(self):
        outcome = ServiceOutcome(RetrievePhoto, self.kwargs)
        obj = outcome.result
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        photo = self._get_photo_with_permission_check()
        outcome = ServiceOutcome(
            ListPhotoVersions, 
            ({"photo": photo} | kwargs)
        )
        data = RetrievePhotoVersionSerializer(outcome.result, many=True).data
        return Response(data, status=status.HTTP_200_OK)