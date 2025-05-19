from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from service_objects.services import ServiceOutcome

from api.views.base_view import BaseView
from api.services import ListPhotos, CreatePhoto
from api.serializers import PageSerializer, PhotoSerializer

class PhotosView(BaseView):
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            ListPhotos,
            request.query_params
        )
        data = PageSerializer(
            instance=outcome.result,
            objects_serializer=PhotoSerializer
        ).data
        return Response(data)

    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            CreatePhoto,
            (request.data | {"user": request.user}),
            request.FILES
        )
        data = PhotoSerializer(outcome.result).data
        return Response(data, status=status.HTTP_201_CREATED)