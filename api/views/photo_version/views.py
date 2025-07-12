from service_objects.services import ServiceOutcome
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from api.views import BaseView
from api.permissions import IsOwner
from api.services import ListPhotoVersions, RetrievePhoto
from api.serializers import RetrievePhotoVersionSerializer
from api.docs import photo_version


class PhotoVersionView(BaseView):
    permission_classes = [IsOwner]

    @extend_schema(**photo_version.list_photo_versions_docs)
    def get(self, request, *args, **kwargs):
        photo = self._get_object_with_permission_check(RetrievePhoto)
        outcome = ServiceOutcome(
            ListPhotoVersions, 
            ({"photo": photo} | kwargs)
        )
        data = RetrievePhotoVersionSerializer(outcome.result, many=True).data
        return Response(data, status=status.HTTP_200_OK)