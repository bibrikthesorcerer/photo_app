from rest_framework import status
from django.urls import reverse

from models_app.factories import LikeFactory, UserProfileFactory, PhotoFactory
from main_app.services import IssueNewUserAPIToken
from api.tests.utils import TempDirectoryAPITestCase


class CreateLikeTest(TempDirectoryAPITestCase):
    @classmethod 
    def setUpTestData(cls):
        cls.test_user = UserProfileFactory.create(user=True)
        cls.user_token = IssueNewUserAPIToken.execute({"user": cls.test_user, "lifetime": 30})
        cls.test_admin = UserProfileFactory.create(admin=True)
        cls.admin_token = IssueNewUserAPIToken.execute({"user": cls.test_admin, "lifetime": 30})
        cls.test_photo = PhotoFactory.create(user=cls.test_user)

    def test_create_like_success_status_201(self):
        response = self.client.post(
            reverse("api:photo_likes", args=[self.test_photo.id]),
            headers={"Authorization": f"Bearer {self.user_token}"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_like_photo_not_found_status_400(self):
        response = self.client.post(
            reverse("api:photo_likes", args=[self.test_photo.id*1000]),
            headers={"Authorization": f"Bearer {self.user_token}"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_like_admins_forbidden_status_403(self):
        response = self.client.post(
            reverse("api:photo_likes", args=[self.test_photo.id]),
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 


class DeleteLikeTest(TempDirectoryAPITestCase):
    @classmethod 
    def setUpTestData(cls):
        cls.test_user = UserProfileFactory.create(user=True)
        cls.user_token = IssueNewUserAPIToken.execute({"user": cls.test_user, "lifetime": 30})
        cls.test_photo = PhotoFactory.create(user=cls.test_user)
        cls.test_like = LikeFactory.create(user=cls.test_user, photo=cls.test_photo)

    def test_delete_like_success_status_200(self):
        response = self.client.delete(
            reverse("api:photo_likes", args=[self.test_photo.id]),
            headers={"Authorization": f"Bearer {self.user_token}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_like_not_found_status_404(self):
        response = self.client.delete(
            reverse("api:photo_likes", args=[self.test_photo.id*1000]),
            headers={"Authorization": f"Bearer {self.user_token}"}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)