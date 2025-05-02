from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from models_app.models import UserProfile
from main_app.services import IssueNewUserAPIToken

class CurrentUserViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('api:current_user')
        self.test_user = UserProfile.objects.create_user(username="testuser", password="testuserpass")
        self.user_token = IssueNewUserAPIToken.execute({"user": self.test_user, "lifetime": 30})

    def test_get_current_user_no_authorization_header(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) # TODO: fix to 401

    def test_get_current_user_with_correct_token(self):
        response = self.client.get(
            self.url,
            headers= {
                "Authorization": f"Bearer {self.user_token}"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_current_user_with_incorrect_token(self):
        response = self.client.get(
            self.url,
            headers= {
                "Authorization": f"Bearer BLAH-BLAH-BLAH"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) # TODO: fix to 401
