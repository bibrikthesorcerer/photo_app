from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from django import forms

from models_app.models import Photo, UserProfile, Comment
from main_app.services import RetrievePhoto
from main_app.services.comment.list import ListComments
from main_app.services.comment.retrieve import RetrieveComment
from notifications.utils import send_message_to_list_of_users


class SendCommentNotification(ServiceWithResult):
    """
    Sends notification to a user whose photo was commented

    Parameters
    ----------
        photo_id (int): id of photo which was commented
        user (UserProfile): user who commented on a photo
    """
    photo_id = forms.IntegerField()
    user = ModelField(UserProfile)

    def process(self) -> None:
        photo_obj = RetrievePhoto.execute({**self.cleaned_data})
        user = self.cleaned_data.get('user')
        # do not notify on self-comment
        if user == photo_obj.user:
            return
        curr_comments = photo_obj.comments_count
        send_message_to_list_of_users(
            [photo_obj.user.id],
            'notify_comment',
            f"User {user} commented on your photo '{photo_obj.title}'. Currently {curr_comments} comments",
            comments_count=curr_comments,
            photo_id=photo_obj.id
        )

class SendCommentWillBeDeletedNotification(ServiceWithResult):
    """
    Sends notification to all users who left comments under a photo scheduled for deletion

    Parameters
    ----------
        photo (Photo): Photo scheduled to be deleted
    """
    photo = ModelField(Photo)

    def process(self) -> None:
        photo_obj = self.cleaned_data.get('photo')
        comments_query = ListComments.execute({"photo_id": photo_obj.id})
        id_list = comments_query.order_by().values_list("user", flat=True).distinct()
        send_message_to_list_of_users(
            id_list,
            'send_notification',
            f"Photo '{photo_obj.title}' which you had commented is scheduled to be deleted with all comments you have left.",
        )

class EditCommentText(ServiceWithResult):
    """
    Edits comment by changing text

    Parameters
    ----------
        comment_id (int): id of comment being edited
        text (str):  new text
    """
    comment_id = forms.IntegerField()
    text = forms.CharField()

    def process(self) -> Comment:
        comment_obj = RetrieveComment.execute({**self.cleaned_data})
        comment_obj.text = self.cleaned_data.get('text')
        comment_obj.save()
        self.result = comment_obj
        return self.result