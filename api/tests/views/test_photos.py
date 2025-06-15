from PIL import Image
from io import BytesIO
from rest_framework import status
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from decouple import config

from models_app.models import Photo
from models_app.factories.user_profile import UserProfileFactory
from models_app.factories import PhotoFactory
from main_app.services import IssueNewUserAPIToken
from api.tests.utils import TempDirectoryAPITestCase


class ListPhotosTest(TempDirectoryAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('api:photos')
        cls.photos = PhotoFactory.create_batch(10)

    def test_get_photos_no_params_status_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_photos_num = Photo.objects.all()[:config('PHOTOS_PER_PAGE', default=20, cast=int)].count()
        self.assertEqual(len(response.data['objects']), expected_photos_num)

    def test_get_photos_with_params_status_200(self):
        response = self.client.get(
            self.url,
            QUERY_STRING=f"per_page=3&page=2&status={Photo.ON_MODERATION}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_photos_num = Photo.objects.filter(status=Photo.ON_MODERATION)[3:6].count()
        self.assertEqual(len(response.data['objects']), expected_photos_num)


class CreatePhotoTest(TempDirectoryAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('api:photos')
        cls.test_user = UserProfileFactory.create()
        cls.user_token = IssueNewUserAPIToken.execute({"user": cls.test_user, "lifetime": 30})
        cls.photos = PhotoFactory.create_batch(10)       

    def test_create_photo_success_status_201(self):
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

    def test_create_photo_invalid_inputs_status_400(self):
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