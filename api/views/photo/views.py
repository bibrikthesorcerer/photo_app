from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from service_objects.services import ServiceOutcome
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

from api.views.base_view import BaseView
from api.services import ListPhotos, CreatePhoto, RetrievePhoto, UpdatePhoto, SchedulePhotoDeletion, RecoverPhotoFromDeletion
from api.serializers import PageSerializer, PhotoSerializer
from api.permissions import IsOwner

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

    @extend_schema(
        summary="Get single Photo using id.",
        parameters=[
            OpenApiParameter(name="photo_id", location="path", type=int, description="id of Photo to be retrieved"),
            OpenApiParameter(name="user", location="query", required=False, type=int,
                             description="id of user, used to add user actions on Photo instance (e.g. is_liked)"
            )
        ],
        responses={
            200: PhotoSerializer,
            404: OpenApiResponse(description="Photo with given id not found")
        },
    )
    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            RetrievePhoto,
            (kwargs | request.query_params),
        )
        data = PhotoSerializer(outcome.result).data
        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Update Photo's information.",
        parameters=[
            OpenApiParameter(name="photo_id", location="path", type=int, description="id of Photo to be updated"),
        ],
        request={
            "img": OpenApiTypes.BINARY,
            "title": OpenApiTypes.STR,
            "description": OpenApiTypes.STR
        },
        responses={
            200: PhotoSerializer,
            400: OpenApiResponse(description="No values for new fields provided"),
            404: OpenApiResponse(description="Photo with given id not found")
        },
    )
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

    @extend_schema(
        summary="Schedule Photo's delayed deletion.",
        parameters=[
            OpenApiParameter(name="photo_id", location="path", type=int, description="id of Photo to be deleted"),
        ],
        responses={
            202: OpenApiResponse(description="Operation scheduled"),
            404: OpenApiResponse(description="Photo with given id not found"),
            410: OpenApiResponse(description="Photo already set to be deleted")
        },
    )
    def delete(self, request, *args, **kwargs):
        photo = self._get_photo_with_permission_check()
        outcome = ServiceOutcome(
            SchedulePhotoDeletion,
            ({"photo": photo} | kwargs),
        )
        return Response(status=status.HTTP_202_ACCEPTED)

class RecoverPhotoView(BaseView):
    permission_classes = [IsOwner]
    
    def _get_photo_with_permission_check(self): # TODO move to BaseView with Retrieve-service as arg, to be DRY
        outcome = ServiceOutcome(RetrievePhoto, self.kwargs)
        obj = outcome.result
        self.check_object_permissions(self.request, obj)
        return obj

    def put(self, request, *args, **kwargs):
        photo = self._get_photo_with_permission_check()
        outcome = ServiceOutcome(
            RecoverPhotoFromDeletion,
            ({"photo": photo} | kwargs)
        )
        return Response(status=status.HTTP_200_OK)