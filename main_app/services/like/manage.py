from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from django.db.models import QuerySet
from django import forms

from main_app.services import RetrievePhoto
from models_app.models import Like, Photo, UserProfile
from notifications.utils import send_message_to_list_of_users

class UpdateOrCreateLike(ServiceWithResult):
    """
    Updates Like object if it is soft deleted
    or creates new Like object if there are no objects with given parameters

    Parameters
    ----------
        photo (Photo): photo associated with like
        user (UserProfile): user associated with like
    """
    photo = ModelField(Photo)
    user = ModelField(UserProfile)

    def process(self) -> QuerySet[Like]:
        photo = self.cleaned_data.get('photo')
        user = self.cleaned_data.get('user')
        self.result, _created = Like.objects.update_or_create(
            photo=photo,
            user=user,
            defaults={"deleted_at": None},
        )
        return self.result
    
class SendLikeNotification(ServiceWithResult):
    """
    Sends notification to a user whose photo was liked or unliked

    Parameters
    ----------
        photo_id (int): id of associated photo
        user (UserProfile): user associated with action
        is_like (bool, optional): True = photo being liked, False = photo being unliked
    """
    photo_id = forms.IntegerField()
    user = ModelField(UserProfile)
    is_like = forms.BooleanField(required=False)

    def process(self) -> None:
        photo_obj = RetrievePhoto.execute({**self.cleaned_data})
        user = self.cleaned_data.get('user')
        # do not notify on self-like
        if user == photo_obj.user:
            return
        
        is_like = self.cleaned_data.get('is_like')
        #change = 1 if is_like else -1
        action = 'liked' if is_like else 'unliked'
        curr_likes = photo_obj.likes_count#+change

        send_message_to_list_of_users(
            [photo_obj.user.id],
            'notify_like',
            f"User {user} {action} your photo '{photo_obj.title}'. Currently {curr_likes} likes",
            likes_count=curr_likes,
            photo_id=photo_obj.id
        )