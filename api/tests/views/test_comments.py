from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from models_app.models import Comment
from models_app.factories.user_profile import UserProfileFactory
from models_app.factories import CommentFactory, PhotoFactory
from main_app.services import IssueNewUserAPIToken
from api.serializers import CommentSerializer

class CommentsViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('api:comments')
        self.test_user = UserProfileFactory.create()
        self.user_token = IssueNewUserAPIToken.execute({"user": self.test_user, "lifetime": 30})
        self.comments = CommentFactory.create_batch(10)
        self.test_photo = PhotoFactory.create()

    def test_get_comments_no_params(self):
        response = self.client.get(self.url)
        expected_comments = [CommentSerializer(comment).data for comment in 
                             sorted(self.comments, key=lambda x: x.pub_date, reverse=True)
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['objects'], expected_comments)

    def test_get_comments_some_params(self):
        response = self.client.get(
            self.url,
            QUERY_STRING="per_page=4&order=pub_date"
        )
        expected_comments = [CommentSerializer(comment).data for comment in 
                        sorted(self.comments, key=lambda x: x.pub_date, reverse=False)
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['objects'], expected_comments[:4])

    def test_create_comment_success(self):
        response = self.client.post(
            self.url,
            data={
                "photo_id": str(self.comments[0].photo.id),
                "parent_id": str(self.comments[0].id),
                "text": "comment text",
            },
            headers= {
                "Authorization": f"Bearer {self.user_token}"
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment_validation_error(self):
        response = self.client.post(
            self.url,
            data={
                "photo_id": str(self.test_photo.id),
                "parent_id": str(self.comments[0].id),
                "text": "comment text",
            },
            headers= {
                "Authorization": f"Bearer {self.user_token}"
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_comment_invalid_inputs_error_missing(self):
        response = self.client.post(
            self.url,
            data={
                "photo_id": str(self.test_photo.id),
                "parent_id": str(self.comments[0].id),
            },
            headers= {
                "Authorization": f"Bearer {self.user_token}"
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_comment_invalid_inputs_error_not_found(self):
        response = self.client.post(
            self.url,
            data={
                "photo_id": 12654165,
                "parent_id": str(self.comments[0].id),
                "text": "blahblahblah"
            },
            headers= {
                "Authorization": f"Bearer {self.user_token}"
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


