from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from models_app.factories.user_profile import UserProfileFactory
from models_app.factories import CommentFactory
from main_app.services import IssueNewUserAPIToken
from api.serializers import RetrieveCommentSerializer


class SingleCommentViewTest(APITestCase):
    def setUp(self):
        self.test_user = UserProfileFactory.create()
        self.user_token = IssueNewUserAPIToken.execute({"user": self.test_user, "lifetime": 30})
        self.test_user2 = UserProfileFactory.create()
        self.user_token2 = IssueNewUserAPIToken.execute({"user": self.test_user2, "lifetime": 30})
        self.test_comment = CommentFactory.create(user=self.test_user)
        self.test_comment_with_child = CommentFactory.create(user=self.test_user, children__num_children=1)
        self.comments = CommentFactory.create_batch(10)

    def test_get_comment_valid_id(self):
        response = self.client.get(
            reverse('api:single_comment', kwargs={"comment_id": self.comments[0].id})
        )
        expected_comment = RetrieveCommentSerializer(self.comments[0]).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_comment)

    def test_get_comment_invalid_id(self):
        response = self.client.get(
            reverse('api:single_comment', kwargs={"comment_id": self.comments[-1].id*10})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_comment_success(self):
        NEW_COMMENT_TEXT = "new comment text"
        response = self.client.put(
            reverse('api:single_comment', kwargs={"comment_id": self.test_comment.id}),
            data={"text": NEW_COMMENT_TEXT},
            format="json",
            headers= {
                "Authorization": f"Bearer {self.user_token}"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_comment = self.test_comment
        expected_comment.text = NEW_COMMENT_TEXT
        expected_comment = RetrieveCommentSerializer(expected_comment).data
        for key in ["updated_at", "deleted_at", "is_delted"]:
            expected_comment.pop(key, None)
            response.data.pop(key, None)
        self.assertEqual(response.data, expected_comment)

    def test_update_comment_not_owner(self):
        NEW_COMMENT_TEXT = "new comment text"
        response = self.client.put(
            reverse('api:single_comment', kwargs={"comment_id": self.test_comment.id}),
            data={"text": NEW_COMMENT_TEXT},
            format="json",
            headers= {
                "Authorization": f"Bearer {self.user_token2}"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_comment_no_body(self):
        response = self.client.put(
            reverse('api:single_comment', kwargs={"comment_id": self.test_comment.id}),
            headers= {
                "Authorization": f"Bearer {self.user_token}"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_comment_invalid_input(self):
        NEW_COMMENT_TEXT = "A"*500
        response = self.client.put(
            reverse('api:single_comment', kwargs={"comment_id": self.test_comment.id}),
            data={"text": NEW_COMMENT_TEXT},
            format="json",
            headers= {
                "Authorization": f"Bearer {self.user_token}"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_success(self):
        response = self.client.delete(
            reverse('api:single_comment', kwargs={"comment_id": self.test_comment.id}),
            headers= {
                "Authorization": f"Bearer {self.user_token}"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data['deleted_at'], None)
        self.assertTrue(response.data['is_deleted'])
        expected_comment = self.test_comment
        expected_comment = RetrieveCommentSerializer(expected_comment).data
        for key in ["updated_at", "deleted_at", "is_deleted"]:
            expected_comment.pop(key, None)
            response.data.pop(key, None)
        
        self.assertEqual(response.data, expected_comment)

    def test_delete_not_owner(self):
        response = self.client.delete(
            reverse('api:single_comment', kwargs={"comment_id": self.test_comment.id}),
            headers= {
                "Authorization": f"Bearer {self.user_token2}"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_with_children(self):
        response = self.client.delete(
            reverse('api:single_comment', kwargs={"comment_id": self.test_comment_with_child.id}),
            headers= {
                "Authorization": f"Bearer {self.user_token}"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data['deleted_at'], None)
        self.assertEqual(response.data['text'], 'DELETED')
        self.assertFalse(response.data['is_deleted'])
        expected_comment = self.test_comment_with_child
        expected_comment = RetrieveCommentSerializer(expected_comment).data
        for key in ["updated_at", "deleted_at", "is_deleted", "text"]:
            expected_comment.pop(key, None)
            response.data.pop(key, None)
        
        self.assertEqual(response.data, expected_comment)
