from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from models_app.factories import PhotoVersionFactory, UserProfileFactory, PhotoFactory, ReviewTicketFactory
from main_app.services import IssueNewUserAPIToken


class ReviewTicketViewTest(APITestCase):
    def setUp(self):
        self.test_user = UserProfileFactory.create()
        self.user_token = IssueNewUserAPIToken.execute({"user": self.test_user, "lifetime": 30})
        self.test_user_2 = UserProfileFactory.create()
        self.user_token_2 = IssueNewUserAPIToken.execute({"user": self.test_user_2, "lifetime": 30})
        self.test_photo = PhotoFactory.create(user=self.test_user)
        self.test_review_ticket_for_photo = ReviewTicketFactory.create(reviewed_object=self.test_photo)
        self.test_version = PhotoVersionFactory.create(photo=self.test_photo)
        self.test_review_ticket = ReviewTicketFactory.create(reviewed_object=self.test_version)

    def test_set_to_seen_success_status_200(self):
        response = self.client.patch(
            reverse("api:review_tickets", args=[self.test_review_ticket.id]),
            headers={"Authorization": f"Bearer {self.user_token}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_set_to_seen_ticket_for_photo_success_status_200(self):
        response = self.client.patch(
            reverse("api:review_tickets", args=[self.test_review_ticket_for_photo.id]),
            headers={"Authorization": f"Bearer {self.user_token}"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_set_to_seen_not_found_status_404(self):
        response = self.client.patch(
            reverse("api:review_tickets", args=[self.test_review_ticket.id*1000]),
            headers={"Authorization": f"Bearer {self.user_token}"}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_set_to_seen_not_owner_status_403(self):
        response = self.client.patch(
            reverse("api:review_tickets", args=[self.test_review_ticket.id]),
            headers={"Authorization": f"Bearer {self.user_token_2}"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_set_to_seen_already_seen_status_400(self):
        self.client.patch(
            reverse("api:review_tickets", args=[self.test_review_ticket.id]),
            headers={"Authorization": f"Bearer {self.user_token}"}
        )
        response = self.client.patch(
            reverse("api:review_tickets", args=[self.test_review_ticket.id]),
            headers={"Authorization": f"Bearer {self.user_token}"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)