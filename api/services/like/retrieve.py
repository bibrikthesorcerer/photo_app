from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound
from django import forms

from models_app.models import Like


class RetrieveLike(ServiceWithResult):
    photo_id = forms.IntegerField()
    user_id = forms.IntegerField()

    def process(self):
        self.result = self._get_like_instance()
        return self

    def _get_like_instance(self):
        photo_id = self.cleaned_data.get("photo_id")
        user_id = self.cleaned_data.get("user_id")
        try:
            return Like.objects.filter(photo_id=photo_id, user_id=user_id).get()
        except Like.DoesNotExist:
            self.add_error(None, NotFound(message="Like with given parameters not found"))
            self.stop_process()