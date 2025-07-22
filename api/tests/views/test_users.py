from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class RegisterUserTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('api:users')
        cls.correct_user_data = {
            "username": "test1",
            "email": "test1@mail.com",
            "password1":"JKASDHgk3892",
            "password2": "JKASDHgk3892"
        }
        cls.password_mismatch_user_data = {
            "username": "test1",
            "email": "test1@mail.com",
            "password1":"test1",
            "password2": "kcdg2"
        }

    def test_register_new_user_success_status_200(self):
        response = self.client.post(
            self.url,
            data=self.correct_user_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_new_duplicate_user_status_400(self):
        self.client.post(
            self.url,
            data=self.correct_user_data
        )
        response = self.client.post(
            self.url,
            data=self.correct_user_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_new_user_password_mismatch_status_400(self):
        response = self.client.post(
            self.url,
            data=self.incorrect_password_user_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
