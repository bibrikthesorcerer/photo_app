from PIL import Image
from io import BytesIO
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.db.models import Count, Q
from django.core.files.uploadedfile import SimpleUploadedFile

from models_app.models import Photo
from models_app.factories.user_profile import UserProfileFactory
from models_app.factories import PhotoFactory
from main_app.services import IssueNewUserAPIToken
from api.serializers import PhotoSerializer, PageSerializer
from django.core.paginator import Paginator

from decouple import config

class PhotosViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('api:photos')
        self.test_user = UserProfileFactory.create()
        self.user_token = IssueNewUserAPIToken.execute({"user": self.test_user, "lifetime": 30})
        self.photos = PhotoFactory.create_batch(10)

    def test_get_photos_no_params(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        expected_photos = Photo.objects.filter().annotate(
                likes_count=Count('like', filter=Q(like__deleted_at=None), distinct=True), 
                comments_count=Count('comment', filter=Q(comment__deleted_at=None), distinct=True))
        
        expected_photos = PageSerializer(
            instance=Paginator(expected_photos, config('PHOTOS_PER_PAGE', cast=int)).get_page(None),
            objects_serializer=PhotoSerializer
            )
        self.assertEqual(response.data['objects'], expected_photos.data['objects'])

    def test_get_photos_with_params(self):
        response = self.client.get(
            self.url,
            QUERY_STRING=f"per_page=3&page=2&status={Photo.ON_MODERATION}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_photos = Photo.objects.filter(status=Photo.ON_MODERATION).annotate(
                likes_count=Count('like', filter=Q(like__deleted_at=None), distinct=True), 
                comments_count=Count('comment', filter=Q(comment__deleted_at=None), distinct=True))
        
        expected_photos = PageSerializer(
            instance=Paginator(expected_photos, 3).get_page(2),
            objects_serializer=PhotoSerializer
            )
        self.assertEqual(response.data['objects'], expected_photos.data['objects'])

    def test_create_photo_success(self):
        img_buffer = BytesIO()
        image = Image.new('RGB', (1,1))
        image.save(img_buffer, format='PNG')
        img_bytes = img_buffer.getvalue()
        response = self.client.post(
            self.url,
            data={
                "img": SimpleUploadedFile("test.png", img_bytes, content_type="image/png"),
                "title": "test image",
                "description": "test description",
            },
            headers={"Authorization": f"Bearer {self.user_token}"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_photo_invalid_inputs(self):
        response = self.client.post(
            self.url,
            data={
                "img": self.photos[0].img,
                "title": "title"*64,
                "description": "description"*256,
            },
            headers={"Authorization": f"Bearer {self.user_token}"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)