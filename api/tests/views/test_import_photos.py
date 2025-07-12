from django.urls import reverse
import json
import os
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey

from models_app.factories import UserProfileFactory


class ImportPhotosTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_user = UserProfileFactory.create(admin=True)
        
        cls.current_dir = os.path.dirname(os.path.abspath(__file__))
        cls.correct_json_data = cls._load_json_data('correct_photo_import.json')
        cls.incorrect_json_data = cls._load_json_data('incorrect_photo_import.json')
        cls.api_key, cls.key = APIKey.objects.create_key(name="test")

    @classmethod
    def _load_json_data(cls, filename):
        file_path = os.path.join(cls.current_dir, filename)
        with open(file_path) as f:
            return json.load(f)

    def test_import_success_200(self):
        response = self.client.post(
            path=reverse("api:import_photos"),
            data=self.correct_json_data,
            headers={"Authorization": f"Api-Key {self.key}"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_import_incorrect_data_400(self):
        response = self.client.post(
            path=reverse("api:import_photos"),
            data=self.incorrect_json_data,
            headers={"Authorization": f"Api-Key {self.key}"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_import_incorrect_api_key_403(self):
        response = self.client.post(
            path=reverse("api:import_photos"),
            data=self.correct_json_data,
            headers={"Authorization": f"Api-Key ${self.key}$"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)