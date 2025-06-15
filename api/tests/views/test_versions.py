from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from models_app.factories import PhotoVersionFactory, UserProfileFactory, PhotoFactory, ReviewTicketFactory
from main_app.services import IssueNewUserAPIToken
from api.tests.utils import TempDirectoryAPITestCase


class ListPhotoVersionsTest(TempDirectoryAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = UserProfileFactory.create()
        cls.user_token = IssueNewUserAPIToken.execute({"user": cls.test_user, "lifetime": 30})
        cls.test_user_2 = UserProfileFactory.create()
        cls.user_token_2 = IssueNewUserAPIToken.execute({"user": cls.test_user_2, "lifetime": 30})
        cls.test_photo = PhotoFactory.create(user=cls.test_user)
        cls.test_version = PhotoVersionFactory.create(photo=cls.test_photo)
        cls.test_review_ticket = ReviewTicketFactory.create(reviewed_object=cls.test_version)

    def test_get_versions_success_status_200(self):
        response = self.client.get(
            reverse("api:photo_versions", args=[self.test_photo.id]),
            headers={"Authorization": f"Bearer {self.user_token}"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_versions_forbidden_status_403(self):
        response = self.client.get(
            reverse("api:photo_versions", args=[self.test_photo.id]),
            headers={"Authorization": f"Bearer {self.user_token_2}"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)