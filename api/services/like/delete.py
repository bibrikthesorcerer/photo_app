from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound
from django import forms

from models_app.models import Like


class DeleteLike(ServiceWithResult):
    photo_id = forms.IntegerField()
    user_id = forms.IntegerField()

    def process(self):
        self.result = self._delete_like()
        return self

    def _delete_like(self):
        photo_id = self.cleaned_data.get('photo_id')
        user_id = self.cleaned_data.get('user_id')
        like_query = Like.objects.filter(photo=photo_id, user=user_id).delete()
        like_obj = like_query.get()
        if like_obj is None:
            self.add_error(None, NotFound(message="Could not find Like with given parameters"))
            self.stop_process()
        return like_obj
