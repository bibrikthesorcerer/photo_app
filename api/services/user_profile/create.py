from django import forms
from django.db import IntegrityError
from service_objects.services import ServiceWithResult
from service_objects.errors import ValidationError
from django.contrib.auth.forms import SetPasswordForm

from models_app.models import UserProfile


class CreateUserProfile(ServiceWithResult):
    username = forms.CharField()
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField()
    password1 = forms.CharField()
    password2 = forms.CharField()

    def process(self) -> UserProfile:
        self.result = self._create_user()
        return self
    
    def _create_user(self) -> UserProfile:
        self.user = UserProfile(
            username=self.cleaned_data.get("username"),
            first_name=self.cleaned_data.get("first_name"),
            last_name=self.cleaned_data.get("last_name"),
            email=self.cleaned_data.get("email")
        )
        self._set_user_password()
        return self.user
    
    def _set_user_password(self):
        form = SetPasswordForm(
            self.user,
            data={
                "new_password1": self.cleaned_data.get("password1"),
                "new_password2": self.cleaned_data.get("password2")
            }
        )
        if not form.is_valid():
            for err_message in form.error_messages.values():
                self.add_error("password1", ValidationError(message=err_message))
                self.stop_process()

        try:
            self.user = form.save()
        except IntegrityError as e:
            self.add_error(None, ValidationError(message=e.args[0]))