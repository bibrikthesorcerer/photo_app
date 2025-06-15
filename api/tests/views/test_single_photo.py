from rest_framework import status
from django.urls import reverse

from models_app.factories.user_profile import UserProfileFactory
from models_app.factories import PhotoFactory, ReviewTicketFactory
from main_app.services import IssueNewUserAPIToken
from models_app.models import PhotoVersion
from api.tests.utils import TempDirectoryAPITestCase


class RetrievePhotoTest(TempDirectoryAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_photo = PhotoFactory.create()

    def test_retrieve_photo_success_status_200(self):
        response = self.client.get(
            reverse("api:single_photo", args=[self.test_photo.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_photo_not_found_status_404(self):
        response = self.client.get(
            reverse("api:single_photo", args=[123])
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdatePhotoTest(TempDirectoryAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = UserProfileFactory.create()
        cls.user_token = IssueNewUserAPIToken.execute({"user": cls.test_user, "lifetime": 30})
        cls.test_photo = PhotoFactory.create(user=cls.test_user)
        cls.test_photo_review_ticket = ReviewTicketFactory.create(reviewed_object=cls.test_photo)

    def test_update_photo_success_status_200(self):
        response = self.client.put(
            reverse("api:single_photo", args=[self.test_photo.id]),
            data={
                "title": "new_title",
                "description": "new_description"
            },
            headers={"Authorization": f"Bearer {self.user_token}"},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), "new_title")
        self.assertEqual(response.data.get('description'), "new_description")
        self.assertTrue(PhotoVersion.objects.filter(photo=self.test_photo).exists())
        ticket = PhotoVersion.objects.prefetch_related('review_tickets').get(photo=self.test_photo).review_tickets.all()[0]
        self.assertTrue(ticket and len(self.test_photo.review_tickets.all()) == 0)

    def test_update_no_fields_failure_status_400(self):
        response = self.client.put(
            reverse("api:single_photo", args=[self.test_photo.id]),
            data={},
            headers={"Authorization": f"Bearer {self.user_token}"},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ScheduleDeletePhotoTest(TempDirectoryAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = UserProfileFactory.create()
        cls.user_token = IssueNewUserAPIToken.execute({"user": cls.test_user, "lifetime": 30})
        cls.test_photo = PhotoFactory.create(user=cls.test_user)

    def test_delete_success_status_202(self):
        response = self.client.delete(
            reverse("api:single_photo", args=[self.test_photo.id]),
            data={},
            headers={"Authorization": f"Bearer {self.user_token}"},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_delete_not_found_status_404(self):
        response = self.client.delete(
            reverse("api:single_photo", args=[self.test_photo.id*1000]),
            data={},
            headers={"Authorization": f"Bearer {self.user_token}"},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_gone_status_410(self):
        request_data = {
            "path":reverse("api:single_photo", args=[self.test_photo.id]),
            "data":{},
            "headers":{"Authorization": f"Bearer {self.user_token}"},
            "format":'json'
        }
        self.client.delete(**request_data)
        response = self.client.delete(**request_data)
        self.assertEqual(response.status_code, status.HTTP_410_GONE)


class RecoverPhotoTest(TempDirectoryAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = UserProfileFactory.create()
        cls.user_token = IssueNewUserAPIToken.execute({"user": cls.test_user, "lifetime": 30})
        cls.test_photo = PhotoFactory.create(user=cls.test_user)

    def test_recover_success_status_200(self):
        request_commons = {
            'data':{},
            'headers':{"Authorization": f"Bearer {self.user_token}"},
            'format':'json'
        }
        self.client.delete(
            reverse("api:single_photo", args=[self.test_photo.id]),
            **request_commons
        )
        response = self.client.put(
            reverse("api:recover_photo", args=[self.test_photo.id]),
            **request_commons
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_recover_not_found_status_404(self):
        response = self.client.put(
            reverse("api:recover_photo", args=[self.test_photo.id*1000]),
            data={},
            headers={"Authorization": f"Bearer {self.user_token}"},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_recover_photo_not_being_deleted_status_400(self):
        response = self.client.put(
            reverse("api:recover_photo", args=[self.test_photo.id]),
            data={},
            headers={"Authorization": f"Bearer {self.user_token}"},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



# class SinglePhotoViewTest(TempDirectoryAPITestCase):
#     def setUp(self):
#         self.test_user = UserProfileFactory.create()
#         self.user_token = IssueNewUserAPIToken.execute({"user": self.test_user, "lifetime": 30})
#         self.test_photo = PhotoFactory.create(user=self.test_user)
#         self.test_photo_review_ticket = ReviewTicketFactory.create(reviewed_object=self.test_photo)

#     def test_retrieve_photo_success_status_200(self):
#         response = self.client.get(
#             reverse("api:single_photo", args=[self.test_photo.id])
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_retrieve_photo_not_found_status_404(self):
#         response = self.client.get(
#             reverse("api:single_photo", args=[123])
#         )
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_update_photo_success_status_200(self):
#         response = self.client.put(
#             reverse("api:single_photo", args=[self.test_photo.id]),
#             data={
#                 "title": "new_title",
#                 "description": "new_description"
#             },
#             headers={"Authorization": f"Bearer {self.user_token}"},
#             format='json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data.get('title'), "new_title")
#         self.assertEqual(response.data.get('description'), "new_description")
#         self.assertTrue(PhotoVersion.objects.filter(photo=self.test_photo).exists())
#         ticket = PhotoVersion.objects.prefetch_related('review_tickets').get(photo=self.test_photo).review_tickets.all()[0]
#         self.assertTrue(ticket and len(self.test_photo.review_tickets.all()) == 0)

#     def test_update_no_fields_failure_status_400(self):
#         response = self.client.put(
#             reverse("api:single_photo", args=[self.test_photo.id]),
#             data={},
#             headers={"Authorization": f"Bearer {self.user_token}"},
#             format='json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_delete_success_status_202(self):
#         response = self.client.delete(
#             reverse("api:single_photo", args=[self.test_photo.id]),
#             data={},
#             headers={"Authorization": f"Bearer {self.user_token}"},
#             format='json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

#     def test_delete_not_found_status_404(self):
#         response = self.client.delete(
#             reverse("api:single_photo", args=[self.test_photo.id*1000]),
#             data={},
#             headers={"Authorization": f"Bearer {self.user_token}"},
#             format='json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_delete_gone_status_410(self):
#         request_data = {
#             "path":reverse("api:single_photo", args=[self.test_photo.id]),
#             "data":{},
#             "headers":{"Authorization": f"Bearer {self.user_token}"},
#             "format":'json'
#         }
#         self.client.delete(**request_data)
#         response = self.client.delete(**request_data)
#         self.assertEqual(response.status_code, status.HTTP_410_GONE)

#     def test_recover_success_status_200(self):
#         request_commons = {
#             'data':{},
#             'headers':{"Authorization": f"Bearer {self.user_token}"},
#             'format':'json'
#         }
#         self.client.delete(
#             reverse("api:single_photo", args=[self.test_photo.id]),
#             **request_commons
#         )
#         response = self.client.put(
#             reverse("api:recover_photo", args=[self.test_photo.id]),
#             **request_commons
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_recover_not_found_status_404(self):
#         response = self.client.put(
#             reverse("api:recover_photo", args=[self.test_photo.id*1000]),
#             data={},
#             headers={"Authorization": f"Bearer {self.user_token}"},
#             format='json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_recover_photo_not_being_deleted_status_400(self):
#         response = self.client.put(
#             reverse("api:recover_photo", args=[self.test_photo.id]),
#             data={},
#             headers={"Authorization": f"Bearer {self.user_token}"},
#             format='json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)