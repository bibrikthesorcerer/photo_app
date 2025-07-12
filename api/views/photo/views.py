from decouple import config
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from service_objects.services import ServiceOutcome
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiRequest
from drf_spectacular.types import OpenApiTypes
from rest_framework_api_key.permissions import HasAPIKey

from api.views.base_view import BaseView
from api.services import (ListPhotos, CreatePhoto, RetrievePhoto,
                          UpdatePhoto, SchedulePhotoDeletion, RecoverPhotoFromDeletion,
                          ImportPhotosList)
from api.serializers import PageSerializer, PhotoSerializer
from api.permissions import IsOwner
from api.docs import photo


class PhotosView(BaseView):
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
    @extend_schema(**photo.list_photos_docs)
    def get(self, request, *args, **kwargs):
        inputs = request.query_params
        if request.user.is_authenticated:
            inputs.update({"user": request.user})
        outcome = ServiceOutcome(
            ListPhotos,
            inputs
        )
        data = PageSerializer(
            instance=outcome.result,
            objects_serializer=PhotoSerializer
        ).data
        return Response(data)

    @extend_schema(**photo.create_photo_docs)
    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            CreatePhoto,
            (request.data | {"user": request.user}),
            request.FILES
        )
        data = PhotoSerializer(outcome.result).data
        return Response(data, status=status.HTTP_201_CREATED)
    

class SinglePhotoView(BaseView):
    def get_permissions(self):
        if self.request.method in ["PUT", "DELETE"]:
            self.permission_classes = [IsOwner]
        return super().get_permissions()
    
    def _get_photo_with_permission_check(self):
        outcome = ServiceOutcome(RetrievePhoto, self.kwargs)
        object = outcome.result
        self.check_object_permissions(self.request, object)
        return object

    @extend_schema(**photo.retrieve_photo_docs)
    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            RetrievePhoto,
            (kwargs | request.query_params),
        )
        data = PhotoSerializer(outcome.result).data
        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(**photo.update_photo_docs)
    def put(self, request, *args, **kwargs):
        if request.data is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        photo = self._get_photo_with_permission_check()
        outcome = ServiceOutcome(
            UpdatePhoto,
            ({"photo":photo} | request.data | kwargs),
            request.data
        )
        data = PhotoSerializer(outcome.result).data
        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(**photo.delete_photo_docs)
    def delete(self, request, *args, **kwargs):
        photo = self._get_photo_with_permission_check()
        outcome = ServiceOutcome(
            SchedulePhotoDeletion,
            ({"photo": photo} | kwargs),
        )
        return Response(status=status.HTTP_202_ACCEPTED)

class RecoverPhotoView(BaseView):
    permission_classes = [IsOwner]
    
    @extend_schema(**photo.recover_photo_docs)
    def put(self, request, *args, **kwargs):
        photo = self._get_object_with_permission_check(RetrievePhoto)
        outcome = ServiceOutcome(
            RecoverPhotoFromDeletion,
            ({"photo": photo} | kwargs)
        )
        return Response(status=status.HTTP_200_OK)
    

class ImportPhotosView(BaseView):
    authentication_classes = []
    permission_classes = [HasAPIKey]

    @extend_schema(**photo.import_photos_docs)
    def post(self, request, *args, **kwargs):
        if type(request.data) != list:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if len(request.data) > config("PHOTO_IMPORT_BATCH_SIZE", cast=int):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        ServiceOutcome(
            ImportPhotosList,
            {"photo_list": request.data}
        )
        return Response(status=200)