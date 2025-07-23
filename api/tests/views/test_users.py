from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from models_app.factories.user_profile.factory import UserProfileFactory

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


class IssueUserTokenTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('api:user_tokens')
        cls.user_password = "JKLfvhidu124"
        cls.user = UserProfileFactory(password=cls.user_password)

    def test_issue_token_success_status_200(self):
        response = self.client.post(
            self.url,
            data={
                "email": self.user.email,
                "password": self.user_password
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_issue_token_incorrect_password_status_401(self):
        response = self.client.post(
            self.url,
            data={
                "email": self.user.email,
                "password": "gibberish"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_issue_token_incorrect_email_status_400(self):
        response = self.client.post(
            self.url,
            data={
                "email": "bademail@bademail.com",
                "password": self.user_password
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteUserTokenTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('api:user_tokens')
        cls.user_password = "JKLfvhidu124"
        cls.user = UserProfileFactory(password=cls.user_password)

    def setUp(self):
        response = self.client.post(
            self.url,
            data={
                "email": self.user.email,
                "password": self.user_password
            }
        )
        self.token = response.data.get("token")
        return super().setUp()
    
    def test_delete_token_success_status_200(self):
        response = self.client.delete(
            self.url,
            headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_token_old_token_use_prohibited_status_401(self):
        self.client.delete(
            self.url,
            headers={"Authorization": f"Bearer {self.token}"}
        )
        response = self.client.delete(
            self.url,
            headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)