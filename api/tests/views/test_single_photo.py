from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.db.models import Count, Q

from models_app.factories.user_profile import UserProfileFactory
from models_app.factories import PhotoFactory, ReviewTicketFactory
from main_app.services import IssueNewUserAPIToken
from api.serializers import PhotoSerializer
from models_app.models import Photo, PhotoVersion, ReviewTicket


class SinglePhotoViewTest(APITestCase):
    def setUp(self):
        self.test_user = UserProfileFactory.create()
        self.user_token = IssueNewUserAPIToken.execute({"user": self.test_user, "lifetime": 30})
        self.test_photo = PhotoFactory.create(user=self.test_user)
        self.test_photo_review_ticket = ReviewTicketFactory.create(reviewed_object=self.test_photo)
        self.dummy_photos = PhotoFactory.create_batch(10)

    def test_retrieve_photo_success(self):
        response = self.client.get(
            reverse("api:single_photo", args=[self.test_photo.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_photo_not_found(self):
        response = self.client.get(
            reverse("api:single_photo", args=[123])
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_photo_success(self):
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
        # TODO check ticket migration
        ticket = PhotoVersion.objects.prefetch_related('review_tickets').get(photo=self.test_photo).review_tickets.all()[0]
        self.assertTrue(ticket and len(self.test_photo.review_tickets.all()) == 0)

    def test_update_no_fields_failure(self):
        response = self.client.put(
            reverse("api:single_photo", args=[self.test_photo.id]),
            data={},
            headers={"Authorization": f"Bearer {self.user_token}"},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)