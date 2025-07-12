from rest_framework import status
from django.urls import reverse
from django.db.models import Q
from decouple import config

from models_app.factories.user_profile import UserProfileFactory
from models_app.factories import CommentFactory, PhotoFactory, ThreadsCommentFactory
from main_app.services import IssueNewUserAPIToken
from api.serializers import CommentSerializer
from api.tests.utils import TempDirectoryAPITestCase
from models_app.models import Comment


class ListCommentsTest(TempDirectoryAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('api:comments')
        cls.test_user = UserProfileFactory.create()
        cls.user_token = IssueNewUserAPIToken.execute({"user": cls.test_user, "lifetime": 30})
        cls.thread = ThreadsCommentFactory(create_thread__thread_depth=3)
        cls.comments = CommentFactory.create_batch(10)

    def test_get_comments_no_params_status_200(self):
        response = self.client.get(self.url)
        expected_comments_num = Comment.objects.filter(
            Q(deleted_at=None) | (Q(text__exact="DELETED") & ~Q(deleted_at=None))
        )[:config('COMMENTS_PER_PAGE', default=20, cast=int)].count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['objects']), expected_comments_num)

    def test_get_comments_some_params_status_200(self):
        response = self.client.get(
            self.url,
            QUERY_STRING="per_page=4&order=pub_date"
        )
        expected_comments_num = Comment.objects.filter(
            Q(deleted_at=None) | (Q(text__exact="DELETED") & ~Q(deleted_at=None))
        ).order_by("pub_date")[:4].count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['objects']), expected_comments_num)

    def test_get_comments_as_thread_status_200(self):
        response = self.client.get(
            self.url,
            QUERY_STRING=f"id={self.thread.id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_comments = [CommentSerializer(self.thread).data]

        def _collect_child_ids(parent):
            children = []
            for child in parent.children.all():
                children.append(CommentSerializer(child).data)
                children.extend(_collect_child_ids(child))
            return children

        expected_comments.extend(_collect_child_ids(self.thread))
        expected_comments = sorted(expected_comments, key=lambda x: x.get('pub_date'), reverse=True)
        self.assertListEqual(response.data['objects'], expected_comments) 


class CreateCommentTest(TempDirectoryAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('api:comments')
        cls.test_user = UserProfileFactory.create()
        cls.user_token = IssueNewUserAPIToken.execute({"user": cls.test_user, "lifetime": 30})
        cls.test_photo = PhotoFactory.create()
        cls.comments = CommentFactory.create_batch(10)

    def test_create_comment_success_status_201(self):
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

    def test_create_comment_validation_error_status_400(self):
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

    def test_create_comment_invalid_inputs_error_missing_status_400(self):
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

    def test_create_comment_invalid_inputs_error_photo_not_found_status_400(self):
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
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)