from service_objects.services import ServiceWithResult, ServiceOutcome
from service_objects.errors import NotFound
from django import forms

from models_app.models import Like
from notifications.utils.senders import send_message_to_list_of_users
from api.services import RetrievePhoto


class DeleteLike(ServiceWithResult):
    photo_id = forms.IntegerField()
    user_id = forms.IntegerField()

    def process(self):
        self.result = self._delete_like()
        self._send_notification_for_photo_author()
        return self

    def _delete_like(self):
        self.photo_id = self.cleaned_data.get('photo_id')
        self.user_id = self.cleaned_data.get('user_id')
        like_query = Like.objects.filter(photo=self.photo_id, user=self.user_id).delete()
        like_obj = like_query.get()
        if like_obj is None:
            self.add_error(None, NotFound(message="Could not find Like with given parameters"))
            self.stop_process()
        return like_obj

    def _send_notification_for_photo_author(self):
        self._get_related_photo()
        if self.photo.user != self.user_id:
            send_message_to_list_of_users(
                [self.photo.user.id],
                "notify_like",
                f"Somebody unliked your photo '{self.photo.title}'. Currently {self.photo.likes_count-1} likes",
                likes_count=self.photo.likes_count-1,
                photo_id=self.photo.id
            )

    def _get_related_photo(self):
        self.photo = ServiceOutcome(
            RetrievePhoto,
            {"photo_id": self.photo_id}
        ).result